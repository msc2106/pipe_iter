from collections.abc import Callable, Iterable, Iterator
import functools
import itertools
import operator
from typing import Any, overload

from .func import star_func, doublestar_func, fallible_func

class Iter:
    def __init__(self, iterable: Iterable, and_mut: bool = False) -> None:
        '''Creates an `Iter` from an iterable object. Note that this uses `iter` and behaves the same as its 1-argument form: iterators are not copied, so exhaustion of the `Iter` will exhaust the original iterator and vice versa. If `and_mut` is `True`, lazy methods return the original `Iter` object; the default behavior is that such methods return a mirror.'''
        self.iterator = iter(iterable)
        self._mutable = and_mut
        self._stars = 0
        self._fail_value = None
        self._fallible = False
    
    def _update(self, iterator: Iterator):
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
        '''Equivalent to `Iter.chained(this, other).copy_settings(this)`.'''
        return Iter.chained(self, other).copy_settings(self)
    
    def __iadd__(self, other: Iterable):
        '''Equivalent to `this = this.chain(other)`. Note that the `mutable` setting of `this` is followed.'''
        return self.chain(other)

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
    
    def _mutating(self):
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
            ._mutating()
            ._update(
                itertools.accumulate(
                    self.iterator,
                    self.wrap_fallible(fn),
                    initial=initial
                )
            )
        )
    
    def apply(self, fn: Callable[[Iterable], Iterator]):
        '''Applies an arbitrary function that takes an iterable and returns an iterator.'''
        return self._mutating()._update(fn(self.iterator))
    
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
            ._mutating()
            ._update(
                itertools.chain(
                    self.iterator, 
                    *iterables
                )
            )
        )
    
    def combinations(self, r: int):
        '''Yields all combinations of `r` elements from the iterator.'''
        return (self
            ._mutating()
            ._update(
                itertools.combinations(
                    self.iterator, 
                    r
                )
            )
        )
    
    def combinations_with_replacement(self, r: int):
        '''Yields all combinations of `r` elements from the iterator, including repeated elements.'''
        return (self
            ._mutating()
            ._update(
                itertools.combinations_with_replacement(
                    self.iterator, 
                    r
                )
            )
        )

    def compress(self, selectors: Iterable[bool]):
        '''Filters the iterator by a selector iterable. The selector iterable must be the same length as the iterator.'''
        return (self
            ._mutating()
            ._update(
                itertools.compress(
                    self.iterator, 
                    selectors
                )
            )
        )

    def cycle(self):
        '''Cycles through the iterator indefinitely.'''
        return (self
            ._mutating()
            ._update(
                itertools.cycle(self.iterator)
            )
        )
    
    def dropwhile(self, predicate: Callable[[Any], bool]):
        '''Drops elements from the iterator while `fn` is `True`. If `fallible`, then the predicate raising an exception will trigger to begin returning values.'''
        return (self
            ._mutating()
            ._update(
                itertools.dropwhile(
                    self.func_options(predicate), 
                    self.iterator
                )
            )
        )
    
    def enumerate(self, start=0):
        '''Enumerates the iterator, starting with `start`.'''
        return (self
            ._mutating()
            ._update(
                enumerate(
                    self.iterator, 
                    start
                )
            )
        )

    def evenitems(self):
        '''Returns every other item of the iterator, starting with the second.'''
        selector = Iter([False, True]).cycle()
        return (self
            ._mutating()
            ._update(
                itertools.compress(
                    self.iterator, 
                    selector
                )
            )
        )

    def filter(self, fn: Callable | None):
        '''Returns an `Iter` of elements for which `fn` is (evaluated as) `True`. If `fn` is `None`, filters out `False`-like values.'''
        return (self
            ._mutating()
            ._update(
                filter(
                    None if fn is None else self.func_options(fn), 
                    self.iterator
                )
            )
        )
    
    def filterfalse(self, fn: Callable | None):
        '''Invers of `filter`: returns an `Iter` of elements for which `fn` is (evaluated as) `False`. If `fn` is `None`, filters out `True`-like values.'''
        return (self
            ._mutating()
            ._update(
                itertools.filterfalse(
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
    
    def flat_map(self, fn: Callable):
        '''Applies a function to each element and flattens the result.'''
        # note: this makes an unecessary copy of the iterator
        return self.map(fn).flatten()
    
    # def fork(self, *predicates: Callable[..., bool], first_only=True) -> list[Fork]:
    #     '''Splits the iterator into a number of iterators equal to the number of predicates. If `first_only=True` (the default) an item is sent to the first iterator for which the predicate is `True`. Otherwise, each iterator contains all elements for which the corresponding predicate is `True`.'''
    #     ...
    
    def flatten(self):
        '''Reduces one level of nesting. Raises `TypeError` if the items of the iterator are not themselves iterable. To keep drop non-iterable items, combine with `filter`. To include non-iterable items as part of the flattening, use `stretch`.'''
        return (self
            ._mutating()
            ._update(
                itertools.chain.from_iterable(self.iterator)
            )
        )

    def groupby(self, key: Callable | None = None):
        '''Groups consecutive items in the iterator by a key function. If `key` is `None`, groups by the identity function. Each iteration returns a tuple of the group key and an iterable of the group items.'''
        return (self
            ._mutating()
            ._update(
                itertools.groupby(
                    self.iterator, 
                    key
                )
            )
        )

    def inspect(self, fn: Callable[[Any], Any]):
        '''Does something with each element of an iterator, passing the **original** value on. This can be used to introduce side-effects to the consumption of the iterator, e.g. to log something for each element. If the iterator is fallible, any exceptions raised by `fn` will be caught and the iterator will continue.'''
        wrapped_function = self.func_options(fn)
        def inspector(x):
            wrapped_function(x)
            return x
        return (self
            ._mutating()
            ._update(
                map(
                    inspector, 
                    self.iterator
                )
            )
        )
    
    @overload
    def islice(self, stop: int | None) -> 'Iter':
        '''Iteration will end after `stop` items'''
        ...

    @overload
    def islice(self, start: int | None, stop: int | None) -> 'Iter':
        '''Slices from `start` (0-indexed) to `stop` (exclusive) or end if `None`'''
        ...
    
    @overload
    def islice(self, start: int | None, stop: int | None, step: int | None = 1) -> 'Iter':
        '''Slices from `start` (0-indexed) to `stop` (exclusive) or end if `None`, with `step`'''
        ...

    def islice(self, *args):
        match args:
            case (start, stop, step):
                new_iter = itertools.islice(self.iterator, start, stop, step)
            case (start, stop):
                new_iter = itertools.islice(self.iterator, start, stop)
            case (step,):
                new_iter = itertools.islice(self.iterator, step)
            case _:
                raise TypeError(f"Invalid arguments {args}")
        return self._mutating()._update(new_iter)
    
    def map(self, fn: Callable[[Any], Any]):
        '''Maps `fn` onto each element of the iterator.'''
        return (self
            ._mutating()
            ._update(
                map(
                    self.func_options(fn), 
                    self.iterator
                )
            )
        )

    def odditems(self):
        '''Returns every other item of the iterator, starting with the first.'''
        selector = Iter([True, False]).cycle()
        return (self
            ._mutating()
            ._update(
                itertools.compress(
                    self.iterator, 
                    selector
                )
            )
        )
    
    def pairwise(self):
        '''Returns pairs of consecutive items from the iterator.'''
        return (self
            ._mutating()
            ._update(
                itertools.pairwise(self.iterator)
            )
        )
    
    def skip(self, n: int):
        '''Skips the first `n` items of the iterator. Alias for `Iter.islice(n, None)`.'''
        return self.islice(n, None)
    
    def somevalue(self):
        '''Filters out `None` values.'''
        return self.filter(lambda x: x is not None)
    
    def starmap(self, fn: Callable):
        '''Maps `fn` onto each element of the iterator, unpacking the arguments. Ignores `star` settings.'''
        return (self
            ._mutating()
            ._update(
                itertools.starmap(
                    self.wrap_fallible(fn), 
                    self.iterator
                )
            )
        )
    
    def stretch(self, level=1, flexible=True):
        '''Reduces `level` levels of nesting. If `flexible` is `True`, items with fewer than `level` levels are included in the result. If `flexible` is `False`, a `TypeError` is raised if the nesting level does not match.'''
        if not isinstance(level, int) or level < 1:
            raise TypeError("level must be a positive integer.")
        def stretch_recur(iterable, current_level):
            for item in iterable:
                if current_level >= level:
                    yield item
                elif isinstance(item, Iterable):
                    for sub_item in stretch_recur(item, current_level + 1):
                        yield sub_item
                else:
                    if flexible:
                        yield item
                    else:
                        raise TypeError(f"Item {item} nested {current_level} levels was not iterable.")

        def stretch_generator(iterator):
            return stretch_recur(iterator, 0)
        
        return self._mutating()._update(stretch_generator(self.iterator))
    
    # def switch_map(self, *conditions: tuple[None | Callable[..., bool], Callable]):
    #     '''Selectively applies functions to elements with a virtual switch statement. The arguments are tuples of a predicate and a function: a given item is transformed by the first function for which the predicate is `True`. If the predicate is `None`, the function is applied to all (remaining) elements.'''
    #     ...

    def take(self, n: int):
        '''Returns the first `n` items of the iterator. Alias for `Iter.islice(n)`.'''
        return self.islice(n)
    
    def takewhile(self, predicate: Callable[[Any], bool]):
        '''Returns items from the iterator while `predicate` is `True`. If `fallible`, then the predicate raising an exception will trigger to stop returning values.'''
        return (self
            ._mutating()
            ._update(
                itertools.takewhile(
                    self.func_options(predicate), 
                    self.iterator
                )
            )
        )
    
    def tee(self, n: int = 2) -> tuple['Iter', ...]:
        '''Creates `n` independent clones.'''
        iterators = itertools.tee(self.iterator, n)
        return tuple(Iter(iterator).copy_settings(self) for iterator in iterators)
    
    def zip(self, *others: Iterable):
        return (self
            ._mutating()
            ._update(
                zip(
                    self.iterator,
                    *others
                )
            )
        )

    def zip_longest(self, *others: Iterable, fillvalue=None):
        return (self
            ._mutating()
            ._update(
                itertools.zip_longest(
                    self.iterator,
                    *others,
                    fillvalue=fillvalue
                )
            )
        )

    #************************#
    #* Combinatoric methods *#
    #************************#
    
    def permutations(self, r: int = None):
        '''Yields all permutations of `r` elements from the iterator. This consumes the original iterator. If `r` is not provided, it defaults to the length of the iterator.'''
        return self._update(
            itertools.permutations(
                self.iterator, 
                r
            )
        )

    def product(self, *iterables, repeat: int = 1):
        '''Yields the cartesian product of the iterator and any number of other iterables. This consumes the iterators (accordingly, `mutating` option is ignored). If `repeat` is provided, each iterator will be repeated that many times.'''
        return self._update(
            itertools.product(
                self.iterator, 
                *iterables, 
                repeat=repeat
            )
        )

    #*********************#
    #* Consuming methods *#
    #*********************#

    def all(self):
        '''Returns `True` if all items in the iterator evaluate to `True`.'''
        return all(self)
    
    def all_not(self):
        '''Returns `True` if all items in the iterator evaluate to `False`.'''
        return not self.any()
    
    def any(self):
        '''Returns `True` if any items in the iterator evaluate to `True`.'''
        return any(self)

    def collect(self, fn: Callable[[Iterable], Any]):
        '''Calls `fn`, function that accepts and consumes an iterable, on itself. For functions that transform an iterable into an `Iterator`, use `apply`.'''
        return fn(self)
    
    def collect_args(self, fn: Callable[..., Any]):
        '''Calls `fn`, a function that accepts positional arguments, by unpacking itself.'''
        return fn(*self)
    
    def count_if(self, predicate: Callable[[Any], bool]):
        '''Counts the number of items in the iterator for which `predicate` is `True`.'''
        return self.filter(predicate).reduce(lambda x, _: x + 1, initial=0)
    
    def find(self, predicate: Callable[[Any], bool]):
        '''Consumes the iterator up to the first item for which `predicate` is `True`, and returns the item. If the iterator is exhausted before finding any such item, returns `None`.'''
        return self.mirror().filter(predicate).next(default=None)
    
    def fold(self, fn: Callable[[Any, Any], Any], initial):
        '''Reduces the iterator to a single value by applying `fn` to each item and the previous result, beginning with `initial`.'''
        return functools.reduce(
            fn,
            self.iterator, 
            initial
        )
    
    def for_each(self, fn: Callable[[Any], Any]) -> None:
        '''Eargerly calls `fn` on each item of iterator.'''
        for item in self:
            self.func_options(fn)(item)

    def next(self, default: Any = ...):
        '''Returns the next item in the iterator. If `default` is provided, it is returned if the iterator is exhausted. Otherwise, `StopIteration` is raised.'''
        if default is ...:
            return next(self)
        else:
            return next(self, default)
        
    def nth(self, n: int):
        '''Returns the `n`th item in the iterator. If the iterator is exhausted before reaching `n`, returns `None`.'''
        for _ in range(n):
            try:
                item = next(self)
            except StopIteration:
                return None
        return item
        
    def reduce(self, fn: Callable[[Any, Any], Any], initial: Any = ...):
        '''Reduces the iterator to a single value by applying `fn` to each item and the previous result. If `initial` is provided, it is used as the initial value.'''
        if initial is ...:
            return functools.reduce(
                fn,
                self.iterator
            )
        else:
            return self.fold(fn, initial)