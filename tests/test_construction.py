from collections.abc import Iterable, Iterator
from pipe_iter import Iter

def test_lazy_eval():
    x = range(10)
    counter = 0
    def foo(x):
        global counter
        counter += 1
        return x+100
    _ = Iter(map(foo, x))
    assert counter == 0

def test_inheritance():
    x = Iter([])
    assert isinstance(x, Iterable)
    assert isinstance(x, Iterator)

def test_from_fn():
    ...

def test_from_args():
    ...

def test_range():
    ...

def test_count():
    ...

def test_repeat():
    ...

def test_chained():
    ...

def test_zipped():
    ...