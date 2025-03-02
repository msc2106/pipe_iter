from pipe_iter import Iter
from pytest import raises

def test_starred():
    lst = list(zip(range(5), range(5, 10)))
    itr1 = Iter(lst)
    itr2 = Iter(lst).star()
    assert itr1.map(lambda x: x[0] + x[1]).collect(list) == [5, 7, 9, 11, 13]
    assert itr2.map(lambda x, y: x + y).collect(list) == [5, 7, 9, 11, 13]

def test_starred_error():
    lst = list(zip(range(5), range(5, 10)))
    itr1 = Iter(lst)
    itr2 = Iter(lst).star()
    with raises(TypeError):
        assert itr1.map(lambda x, y: x + y).collect(list) == [5, 7, 9, 11, 13]
    with raises(TypeError):
        assert itr2.map(lambda x: x[0] + x[1]).collect(list) == [5, 7, 9, 11, 13]

def test_fallible():
    lst = [0, 1, None, 2, 3]
    itr1 = Iter(lst).map(int)
    itr2 = Iter(lst).fallible().map(int)
    with raises(TypeError):
        _ = itr1.collect(list)
    assert itr2.collect(list) == lst

def test_fail_value():
    lst = [0, 1, None, 2, 3]
    itr = Iter(lst).fallible(fail_value=0).map(int) 
    assert itr.collect(list) == [0, 1, 0, 2, 3]