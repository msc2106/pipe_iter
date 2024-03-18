from typing import Iterable, Callable

class PipeIter:
    def __init__(self, iterator: Iterable) -> None:
        self.iterator = iter(iterator) # this will not trigger evaluation of a map or filter object
    
    def __iter__(self):
        return iter(self.iterator)
    
    def __next__(self):
        return next(self.iterator)
    
    def map(self, fn: Callable):
        return PipeIter(
            map(
                fn, 
                self.iterator
            )
        )
    
    def filter(self, fn: Callable):
        return PipeIter(
            filter(
                fn, 
                self.iterator
            )
        )
    
    def filter_map(self, fn: Callable):
        filter_fn = lambda item: item is not None
        return PipeIter(
            self.map(fn)
                .filter(filter_fn)
        )
    
    def collect(self, fn: Callable):
        return fn(self.iterator)