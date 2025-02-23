from pipe_iter import Iter
from pytest import raises

def test_chained():
    x = list(range(5))
    y = list("ABCD")
    itr = Iter.chained(x, y)
    assert itr.collect(list) == x + y

def test_clone():
    x = range(2)
    itr1 = Iter(x)
    itr2 = itr1.clone().map(lambda x: x * 2)
    assert next(itr1) == 0
    assert next(itr2) == 0
    assert next(itr2) == 2
    assert next(itr1) == 1

def test_count():
    start = 2
    step = 3
    counter = Iter.count(start, step)
    val = start
    for _ in range(10):
        assert next(counter) == val
        val += step

def test_from_args():
    lst1 = list(range(5))
    s = "ABCDE"
    lst2 = list(s)
    itr1 = Iter.from_args(*lst1)
    itr2 = Iter.from_args(*lst2)
    assert list(itr1) == lst1
    assert "".join(itr2) == s

def test_from_fn():
    lst = list(range(5))
    def count_down(lst=lst):
        if lst:
            return lst.pop()
        else:
            return None
    
    itr = Iter.from_fn(count_down, None)
    assert list(itr) == list(range(4, -1, -1))

def test_from_kwargs():
    d = {
        key: value
        for key, value in zip("ABCDE", range(5))
    }
    itr = Iter.from_kwargs(**d)
    assert list(itr) == list(d.items())

def test_mirror():
    itr1 = Iter(range(10))
    itr2 = itr1.mirror().map(lambda x: x * 2)
    assert next(itr1) == 0
    assert next(itr2) == 2
    assert next(itr2) == 4
    assert next(itr1) == 3

def test_range():
    assert list(Iter.range(5)) == list(range(5))
    assert list(Iter.range(5, 15, 2)) == list(range(5, 15, 2))

def test_repeat():
    val = 'x'
    n = 50
    
    itr = Iter.repeat(val, n)
    assert itr.collect(list) == [val] * n
    
    itr_indefinite = Iter.repeat(val)
    for _ in range(n):
        assert val == next(itr_indefinite)
    
    empty_itr = Iter.repeat(val, 0)
    assert empty_itr.collect(list) == []

    with raises(TypeError):
        Iter.repeat(val, val)

def test_zipped():
    x = range(3)
    y = range(5)
    z = "ABCD"

    itr1 = Iter.zipped(x, y, z)
    assert itr1.collect(list) == [
        (0, 0, 'A'),
        (1, 1, 'B'),
        (2, 2, 'C')
    ]

    itr2 = Iter.zipped(x, y, z, strict=True)
    with raises(ValueError):
        itr2.collect(list)

    itr3 = Iter.zipped(range(3), z[:3], strict=True)
    assert itr3.collect(list) == [
        (0, 'A'),
        (1, 'B'),
        (2, 'C')
    ]