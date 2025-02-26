from collections.abc import Iterable, Callable, Mapping
from typing import Any

def doublestar_func(fn: Callable[..., Any], convert=True):
    '''Wraps `fn` to unpack mapping arguments. With `convert=True`, the default, tries to convert the argument to a `dict` (e.g. collections of duples).'''
    return fn

def fallible_func(fn: Callable[[Any], Any], fail_value: Any | None = None):
    '''Wraps `fn` to catch exceptions and return `fail_value`.'''
    return fn

def star_func(fn: Callable[..., Any], strict=True):
    '''Wraps `fn` to unpack iterable single arguments. With `strict=True`, the default, follows behavior of `itertools.starmap` by raising `TypeError` if non-iterable arguments is passed. With `strict=False`, non-iterable arguments are passed as is.'''
    def new_fn(arg: Iterable):
        return fn(*arg) if strict or isinstance(arg, Iterable) else fn(arg)
    return new_fn