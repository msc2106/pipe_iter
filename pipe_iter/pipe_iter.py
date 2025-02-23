from collections.abc import Iterable, Callable
import itertools
from typing import Any

class Iter:
    @staticmethod
    def func_options(method: Callable[..., Any]):
        ...

    def __init__(self, iterable: Iterable) -> None:
        '''Creates an `Iter` from an iterable object. Note that this uses `iter` and behaves the same as its 1-argument form: iterators are not copied, so exhaustion of the `Iter` will exhaust the original iterator and vice versa.'''
        self.iterator = iter(iterable)
        self._stars = 0
        self._fail_value = None
        self._fallible = False
    
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
    
    def clone(self):
        '''Uses `itertools.tee` to create an independent copy of the iterator, preserving this `Iter`'s settings.'''
        self.iterator, new_iterator = itertools.tee(self.iterator)
        new_iter = Iter(new_iterator).copy_settings(self)
        return new_iter
    
    def mirror(self):
        '''Returns a new `Iter` that shares the same underlying iterator.'''
        new_iter = Iter(self.iterator).copy_settings(self)
        return new_iter
    
    #*****************#
    #* Magic methods *#
    #*****************#

    def __add__(self, other: Iterable):
        raise NotImplementedError()
    
    def __iadd__(self, other: Iterable):
        raise NotImplementedError()

    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.iterator)

    #********************#
    #* Settings methods *#
    #********************#

    def copy_settings(self, other_iter):
        '''Copies the settings of another `Iter` object.'''
        if not isinstance(other_iter, Iter):
            raise TypeError("Argument must be an Iter object.")
        self._stars = other_iter._stars
        self._fail_value = other_iter._fail_value
        self._fallible = other_iter._fallible
        return self

    def doublestar(self):
        '''Subsequent functions added to the evaluation chain will be wrapped with `doublestar_func`, receiving keyword arguments. Overrides `star`.'''
        self._stars = 2
        return self
    
    def fallible(self, fail_value=None):
        '''Subsequent functions added to the evaluation chain will be wrapped with `fallible_func`, catching any errors raised and instead returning return of `fail_value` (default `None`).'''
        self._fallible = True
        self._fail_value = fail_value
        return self
    
    def star(self):
        '''Subsequent functions added to the evaluation change will be wrapped with `star_func`, receiving unpacked arguments. Overrides `doublestar`.'''
        self._stars = 1
        return self
    
    def unset_fallible(self):
        '''Any errors raised by subsequent functions in the evaluation chain will be propagated.'''
        self._fallible = True
        return self
    
    def unset_stars(self):
        '''Subsequent functions added to the evaluation change will receive single arguments.'''
        self._stars = 0
        return self

    #****************#
    #* Lazy methods *#
    #****************#

    def map(self, fn: Callable[[Any], Any]):
        '''Lazily calls `fn` (which must accept a single positional argument) on each element of the iterator.'''
        self.iterator = map(
            fn, 
            self.iterator
        )
        return self
    
    def filter(self, fn: Callable | None):
        '''Returns an `Iter` of elements for which `fn` is (evaluated as) `True`. If `fn` is `None`, filters out non-`True` values.'''
        self.iterator = filter(
            fn, 
            self.iterator
        )
        return self
    
    def filter_map(self, fn: Callable):
        '''Applies a function to each element, and filters out `None` results.'''
        def filter_fn(item):
            return item is not None
        return self.map(fn).filter(filter_fn)
    
    #*********************#
    #* Consuming methods *#
    #*********************#

    def collect(self, fn: Callable[[Iterable], Any]):
        '''Calls `fn`, function that accepts and consumes an iterable, on itself. For functions that transform an iterable into an `Iterator`, use `apply`.'''
        return fn(self)
    
    def collect_args(self, fn: Callable[..., Any]):
        '''Calls `fn`, a function that accepts positional arguments, by unpacking itself.'''
        return fn(*self)