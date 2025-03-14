from collections.abc import Iterable, Callable, Mapping
from typing import Any

def doublestar_func(fn: Callable[..., Any], convert=True):
    '''Wraps `fn` to unpack mapping arguments. With `convert=True`, the default, tries to convert the argument to a `dict` (e.g. collections of duples).'''
    def new_fn(val: Mapping | Iterable):
        kwargs = dict(val) if convert else val
        return fn(**kwargs)
    return new_fn

def fallible_func(fn: Callable[[Any], Any], fail_value: Any | None = None):
    '''Wraps `fn` to catch exceptions and return `fail_value`.'''
    def new_fn(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            return fail_value
    return new_fn

def star_func(fn: Callable[..., Any], strict=True):
    '''Wraps `fn` to unpack iterable single arguments. With `strict=True`, the default, follows behavior of `itertools.starmap` by raising `TypeError` if non-iterable arguments is passed. With `strict=False`, non-iterable arguments are passed as is.'''
    def new_fn(arg: Iterable):
        return fn(*arg) if strict or isinstance(arg, Iterable) else fn(arg)
    return new_fn