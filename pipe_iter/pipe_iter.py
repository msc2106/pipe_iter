from collections.abc import Iterable, Callable
from typing import Any

class Iter:
    def __init__(self, iterable: Iterable) -> None:
        '''Creates an `Iter` from an iterable object. Note that this uses `iter`, so behaves the same as it: iterators are not copied, so exhaustion of the `Iter` will exhaust the original iterator and vice versa.'''
        self.iterator = iter(iterable)
    
    @classmethod
    def from_fn(cls, fn: Callable[[], Any], sentinel):
        return cls(iter(fn, sentinel))
    
    @classmethod
    def from_args(cls, *elements):
        return cls(elements)

    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.iterator)
    
    def map(self, fn: Callable):
        return Iter(
            map(
                fn, 
                self.iterator
            )
        )
    
    def filter(self, fn: Callable | None):
        return Iter(
            filter(
                fn, 
                self.iterator
            )
        )
    
    def filter_map(self, fn: Callable):
        '''Applies a function to each element, and filters out `None` results.'''
        def filter_fn(item):
            return item is not None
        return Iter(
            self.map(fn)
                .filter(filter_fn)
        )
    
    def collect(self, fn: Callable[[Iterable], Any]):
        return fn(self.iterator)
    
    def collect_args(self, fn: Callable[..., Any]):
        return fn(*self.iterator)