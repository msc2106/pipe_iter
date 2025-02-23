from typing import Callable, Any

def star_func(fn: Callable[..., Any]):
    ...

def doublestar_func(fn: Callable[..., Any]):
    ...

def fallible_func(fn: Callable[[Any], Any]):
    ...