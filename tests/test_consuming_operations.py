from pipe_iter import Iter
from pytest import raises

def test_all():
    assert Iter([True, 'A', 1]).all()
    assert not Iter([True, 'A', 0]).all()

def test_all_not():
    assert Iter([False, None, 0, '']).all_not()
    assert not Iter([False, None, 1, 'A']).all_not()

def test_any():
    assert Iter([False, None, 1, 'A']).any()
    assert not Iter([False, None, 0, '']).any()

def test_collect():
    assert Iter([1, 2, 3]).collect(list) == [1, 2, 3]
    assert Iter([1, 2, 3]).collect(tuple) == (1, 2, 3)
    assert Iter([1, 2, 3]).collect(set) == {1, 2, 3}
    assert Iter([1, 2, 3]).map(str).collect(lambda itr: ''.join(itr)) == '123'

def test_collect_args():
    def foo(*args):
        return ', '.join(f"{i} {arg}" for i, arg in enumerate(args))
    assert Iter([1, 2, 3]).collect_args(foo) == '0 1, 1 2, 2 3'

def test_count_if():
    assert Iter(range(10)).count_if(lambda x: x % 2) == 5

def test_eq():
    ...

def test_find():
    itr = Iter(range(10))
    assert itr.find(lambda x: x % 2 == 1) == 1
    assert next(itr) == 2
    assert itr.find(lambda x: x > 10) is None
    with raises(StopIteration):
        next(itr)

def test_fold():
    assert Iter(range(10)).fold(lambda acc, x: acc + x, 0) == 45
    assert Iter(range(10)).fold(lambda acc, x: acc + x, 1) == 46
    with raises(TypeError):
        assert Iter(range(10)).fold(lambda acc, x: acc + x) == 45

def test_for_each():
    ...

def test_neq():
    ...

def test_next():
    ...

def test_next_method():
    ...

def test_nth():
    ...

def test_partition():
    ...

def test_position():
    ...

def test_reduce():
    assert Iter(range(10)).reduce(lambda acc, x: acc + x, 0) == 45
    assert Iter(range(10)).reduce(lambda acc, x: acc + x, 1) == 46
    assert Iter(range(10)).reduce(lambda acc, x: acc + x) == 45

def test_unzip():
    ...