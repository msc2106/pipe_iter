from collections.abc import Iterable, Callable
import itertools
from typing import Any

class Iter:
    def __init__(self, iterable: Iterable) -> None:
        '''Creates an `Iter` from an iterable object. Note that this uses `iter`, so behaves the same as it: iterators are not copied, so exhaustion of the `Iter` will exhaust the original iterator and vice versa.'''
        self.iterator = iter(iterable)
    
    #************************#
    #* Construction methods *#
    #************************#

    @classmethod
    def count(cls, start=0, step=1):
        '''Creates an `Iter` that behaves like `itertools.count`: an infinite series of numerical values beginning with `start` and incremented by `step`.'''
        return cls(itertools.count(start, step))
    
    @classmethod
    def from_args(cls, *elements):
        '''Creates an `Iter` from a positional arguments.'''
        return cls(elements)
    
    @classmethod
    def from_fn(cls, fn: Callable[[], Any], sentinel):
        '''Creates an `Iter` from a function that returns elements until a sentinel value is returned. This reflects the 2-argument version of the built-in `iter` function.'''
        return cls(iter(fn, sentinel))
    
    @classmethod
    def from_kwargs(cls, **elements):
        '''Creates an `Iter` from keyword arguments.'''
        return cls(elements.items())

    @classmethod
    def range(cls, range_arg: int, stop: int | None = None, step: int = 1):
        '''Creates an `Iter` that behaves like `range`, except that `step` can be set even if `stop` is not. That is to say, if `stop` is not provided, it produces integers from 0 up to `range_arg` (exclusive) by `step`. If `stop` is provided, it produces integers from `range_arg` up to `stop` (exclusive) by `step`.'''
        start = 0 if stop is None else range_arg
        end = range_arg if stop is None else stop
        return cls(range(start, end, step))
    
    #*****************#
    #* Magic methods *#
    #*****************#

    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.iterator)

    #****************#
    #* Lazy methods *#
    #****************#

    def map(self, fn: Callable[[Any], Any]):
        '''Lazily calls `fn` (which must accept a single positional argument) on each element of the iterator.'''
        return Iter(
            map(
                fn, 
                self.iterator
            )
        )
    
    def filter(self, fn: Callable | None):
        '''Returns an `Iter` of elements for which `fn` is (evaluated as) `True`. If `fn` is `None`, filters out non-`True` values.'''
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
    
    #*********************#
    #* Consuming methods *#
    #*********************#

    def collect(self, fn: Callable[[Iterable], Any]):
        '''Calls `fn`, function that accepts and consumes an iterable, on itself. For functions that transform an iterable into an `Iterator`, use `apply`.'''
        return fn(self)
    
    def collect_args(self, fn: Callable[..., Any]):
        '''Calls `fn`, a function that accepts positional arguments, by unpacking itself.'''
        return fn(*self)