from collections import deque
from .pipe_iter import Iter

class Fork:
    '''An Iterator that as part of a set shares an underlying iterator, dividing items among them according to defined rules.'''

    @classmethod
    def fork(cls, iterator: Iter, *predicates):
        forks: list[Fork] = []
        rules = []
        for predicate in predicates:
            fork = Fork()
            forks.append(fork)
            rules.append((predicate, fork))
        match iterator._stars:
            case 0:
                def forker(val):
                    forks = Iter(rules) \
                        .star() \
                        .filter_map(lambda predicate, fork: fork if predicate(val) else None) \
                        .collect(list)
                    return val, forks
            case 1:
                def forker(*vals):
                    forks = Iter(rules) \
                        .star() \
                        .filter_map(lambda predicate, fork: fork if predicate(*vals) else None) \
                        .collect(list)
                    return vals, forks
            case 2:
                def forker(**kwargs):
                    forks = Iter(rules) \
                        .star() \
                        .filter_map(lambda predicate, fork: fork if predicate(**kwargs) else None) \
                        .collect(list)
                    return kwargs, forks
            case _:
                raise ValueError("Corrupted Iter: invalid _stars value")
        return [fork.setup(iterator.mirror().map(forker)) for fork in forks]
        
    def __init__(self):
        self.iterator: Iter = None
        self.buffer = deque()

    def setup(self, iterator: Iter):
        self.iterator = iterator
        return self
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.iterator is None:
            raise ValueError("Fork not properly initialized.")
        found_one = False
        next_val = None
        if self.buffer:
            return self.buffer.popleft()
        while not found_one:
            val, forks = next(self.iterator)
            for fork in forks:
                if fork is self:
                    found_one = True
                    next_val = val
                else:
                    fork.buffer.append(val)
        return next_val