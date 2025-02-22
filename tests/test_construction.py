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
    lst = list(range(5))
    def count_down(lst=lst):
        if lst:
            return lst.pop()
        else:
            return None
    
    itr = Iter.from_fn(count_down, None)
    assert list(itr) == list(range(4, -1, -1))

def test_from_args():
    lst1 = list(range(5))
    s = "ABCDE"
    lst2 = list(s)
    itr1 = Iter.from_args(*lst1)
    itr2 = Iter.from_args(*lst2)
    assert list(itr1) == lst1
    assert "".join(itr2) == s

def test_from_kwargs():
    d = {
        key: value
        for key, value in zip("ABCDE", range(5))
    }
    itr = Iter.from_kwargs(**d)
    assert list(itr) == list(d.items())

def test_range():
    assert list(Iter.range(5)) == list(range(5))
    assert list(Iter.range(5, 15, 2)) == list(range(5, 15, 2))

def test_count():
    start = 2
    step = 3
    counter = Iter.count(start, step)
    val = start
    for _ in range(10):
        assert next(counter) == val
        val += step

def test_repeat():
    ...

def test_chained():
    ...

def test_zipped():
    ...