from collections.abc import Callable, Iterable, Iterator
import itertools
import operator
from typing import Any

from .func import star_func, doublestar_func, fallible_func

class Iter:
    def __init__(self, iterable: Iterable, and_mut: bool = False) -> None:
        '''Creates an `Iter` from an iterable object. Note that this uses `iter` and behaves the same as its 1-argument form: iterators are not copied, so exhaustion of the `Iter` will exhaust the original iterator and vice versa. If `and_mut` is `True`, lazy methods return the original `Iter` object; the default behavior is that such methods return a mirror.'''
        self.iterator = iter(iterable)
        self._mutable = and_mut
        self._stars = 0
        self._fail_value = None
        self._fallible = False
    
    def update(self, iterator: Iterator):
        '''Updates the iterator.'''
        self.iterator = iterator
        return self

    #************************#
    #* Construction methods *#
    #************************#

    @classmethod
    def and_mut(cls, iterable: Iterable):
        '''Creates an `Iter` from an iterable and sets it to be mutable.'''
        return cls(iterable, and_mut=True)

    @classmethod
    def chained(cls, *iterables, and_mut: bool = False):
        '''Creates an `Iter` that chains together multiple iterables.'''
        return cls(itertools.chain(*iterables), and_mut=and_mut)
    
    @classmethod
    def count(cls, start=0, step=1, and_mut: bool = False):
        '''Creates an `Iter` that behaves like `itertools.count`: an infinite series of numerical values beginning with `start` and incremented by `step`.'''
        return cls(itertools.count(start, step), and_mut=and_mut)
    
    @classmethod
    def from_args(cls, *elements, and_mut: bool = False):
        '''Creates an `Iter` from a positional arguments.'''
        return cls(elements, and_mut=and_mut)
    
    @classmethod
    def from_fn(cls, fn: Callable[[], Any], sentinel, and_mut: bool = False):
        '''Creates an `Iter` from a function that returns elements until a sentinel value is returned. This reflects the 2-argument version of the built-in `iter` function.'''
        return cls(iter(fn, sentinel), and_mut=and_mut)
    
    @classmethod
    def from_kwargs(cls, and_mut: bool = False, **elements):
        '''Creates an `Iter` from keyword arguments.'''
        return cls(elements.items(), and_mut=and_mut)

    @classmethod
    def range(cls, range_arg: int, stop: int | None = None, step: int = 1, and_mut: bool = False):
        '''Creates an `Iter` that behaves like `range`, except that `step` can be set even if `stop` is not. That is to say, if `stop` is not provided, it produces integers from 0 up to `range_arg` (exclusive) by `step`. If `stop` is provided, it produces integers from `range_arg` up to `stop` (exclusive) by `step`.'''
        start = 0 if stop is None else range_arg
        end = range_arg if stop is None else stop
        return cls(range(start, end, step), and_mut=and_mut)
    
    @classmethod
    def zipped(cls, *iterables, strict=False, and_mut: bool = False):
        '''Creates an `Iter` that yields tuples of elements from the provided iterables. If `strict` is `False`, the default, iteration stops when the shortest iterable is exhausted. If `strict` is `True`, a `ValueError` is raised instead of `StopIteration` if not all of the iteratables are exhausted together.'''
        return cls(zip(*iterables, strict=strict), and_mut=and_mut)

    def clone(self):
        '''Uses `itertools.tee` to create an independent copy of the iterator, preserving this `Iter`'s settings.'''
        self.iterator, new_iterator = itertools.tee(self.iterator)
        new_iter = Iter(new_iterator).copy_settings(self)
        return new_iter
    
    def mirror(self):
        '''Returns a new `Iter` that shares the same underlying iterator.'''
        new_iter = Iter(self.iterator).copy_settings(self)
        return new_iter
    
    @classmethod
    def repeat(cls, item, n=None, and_mut: bool = False):
        '''Creates an `Iter` that repeats `item` `n` times. If `n` is `None` (the default), the iterator will repeat indefinitely. If `n` is less than 1, the iterator will be empty.'''
        match n:
            case None:
                return cls(itertools.repeat(item), and_mut=and_mut)
            case int():
                return cls(itertools.repeat(item, n), and_mut=and_mut)
            case _:
                raise TypeError("If not provided and not None, n must be an integer.")
    
    
    #*****************#
    #* Magic methods *#
    #*****************#

    def __add__(self, other: Iterable):
        '''Equilvalent to `Iter.chained(this, other).copy_settings(this)`.'''
        raise NotImplementedError()
    
    def __iadd__(self, other: Iterable):
        '''Equivalent to `this = this.chain(other)`. Note that the `mutable` setting of `this` is followed.'''
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
        self._mutable = other_iter._mutable
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
    
    def mutating(self):
        if self._mutable:
            return self
        else:
            return self.mirror()
    
    def wrap_fallible(self, fn: Callable):
        if self._fallible:
            return fallible_func(fn, fail_value=self._fail_value)
        else:
            return fn
        
    def func_options(self, fn: Callable):
        def identity(x: Callable):
            return x
        inner = doublestar_func if self._stars == 2 else star_func if self._stars == 1 else identity
        return self.wrap_fallible(inner(fn))

    #****************#
    #* Lazy methods *#
    #****************#
    
    def accumulate(self, fn: Callable[[Any, Any], Any] = operator.add, initial=None):
        '''Applies a function to each element and the previous result, starting with `initial`. The result of each function call is yielded. Is not effected by star settings.'''
        return (self
            .mutating()
            .update(
                itertools.accumulate(
                    self.iterator,
                    self.wrap_fallible(fn),
                    initial=initial
                )
            )
        )
    
    def apply(self, fn: Callable[[Iterable], Iterator]):
        '''Applies an arbitrary function that takes an iterable and returns an iterator.'''
        return self.mutating().update(fn(self.iterator))
    
    def batched(self, n: int, *, fillvalue=...):
        '''Yields tuples of `n` elements at a time. If `fillvalue` is specified, the last batch will be filled with it if necessary, otherwise the last batch batch might be smaller than `n`.'''
        def batch_generator(iterator):
            exhausted = False
            while not exhausted:
                batch = []
                for _ in range(n):
                    try:
                        batch.append(next(iterator))
                    except StopIteration:
                        exhausted = True
                        if fillvalue is not ...:
                            batch.append(fillvalue)
                        else:
                            break
                yield tuple(batch)
        return self.apply(batch_generator)
    
    def chain(self, *iterables):
        '''Appends one or more other iterables to the iterator.'''
        return (self
            .mutating()
            .update(
                itertools.chain(
                    self.iterator, 
                    *iterables
                )
            )
        )
    
    def combinations(self, r: int):
        '''Yields all combinations of `r` elements from the iterator.'''
        return (self
            .mutating()
            .update(
                itertools.combinations(
                    self.iterator, 
                    r
                )
            )
        )
    
    def combinations_with_replacement(self, r: int):
        '''Yields all combinations of `r` elements from the iterator, including repeated elements.'''
        return (self
            .mutating()
            .update(
                itertools.combinations_with_replacement(
                    self.iterator, 
                    r
                )
            )
        )

    def filter(self, fn: Callable | None):
        '''Returns an `Iter` of elements for which `fn` is (evaluated as) `True`. If `fn` is `None`, filters out non-`True` values.'''
        return (self
            .mutating()
            .update(
                filter(
                    None if fn is None else self.func_options(fn), 
                    self.iterator
                )
            )
        )
    
    def filter_map(self, fn: Callable):
        '''Applies a function to each element, and filters out `None` results.'''
        return (self
            .map(self.func_options(fn))
            .somevalue()
        )
    
    # def fork(self, *predicates: Callable[..., bool], first_only=True) -> list[Fork]:
    #     '''Splits the iterator into a number of iterators equal to the number of predicates. If `first_only=True` (the default) an item is sent to the first iterator for which the predicate is `True`. Otherwise, each iterator contains all elements for which the corresponding predicate is `True`.'''
    #     ...
    
    
    def map(self, fn: Callable[[Any], Any]):
        '''Maps `fn` onto each element of the iterator.'''
        return (self
            .mutating()
            .update(
                map(
                    self.func_options(fn), 
                    self.iterator
                )
            )
        )
    
    def somevalue(self):
        '''Filters out `None` values.'''
        return self.filter(lambda x: x is not None)
    
    def switch_map(self, *conditions: tuple[None | Callable[..., bool], Callable]):
        '''Selectively applies functions to elements with a virtual switch statement. The arguments are tuples of a predicate and a function: a given item is transformed by the first function for which the predicate is `True`. If the predicate is `None`, the function is applied to all (remaining) elements.'''
        ...

    #*********************#
    #* Consuming methods *#
    #*********************#

    def collect(self, fn: Callable[[Iterable], Any]):
        '''Calls `fn`, function that accepts and consumes an iterable, on itself. For functions that transform an iterable into an `Iterator`, use `apply`.'''
        return fn(self)
    
    def collect_args(self, fn: Callable[..., Any]):
        '''Calls `fn`, a function that accepts positional arguments, by unpacking itself.'''
        return fn(*self)