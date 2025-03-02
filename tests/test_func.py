from pipe_iter import star_func, doublestar_func, fallible_func, Iter
from pytest import raises

def test_doublestarfunc():
    ...

def test_doublestarfunc_invalid():
    ...

def test_falliblefunc():
    lst = [0, 1, None, 2, 3]
    itr1 = Iter(lst).map(int)
    itr2 = Iter(lst).map(fallible_func(int))
    with raises(TypeError):
        _ = itr1.collect(list)
    assert itr2.collect(list) == lst

def test_fail_value():
    lst = [0, 1, None, 2, 3]
    assert Iter(lst).map(fallible_func(int, fail_value=0)).collect(list) == [0, 1, 0, 2, 3]

def test_starfunc():
    r = range(10)
    product = Iter.zipped(r, r).map(star_func(lambda x, y: x * y)).collect(list)
    assert product == [x**2 for x in r]

def test_starfunc_invalid():
    r = range(10)
    with raises(TypeError):
        _ = Iter(r).map(star_func(lambda x: x)).collect(list)
    list(r) == Iter(r).map(star_func(lambda x: x, strict=False)).collect(list)

def test_stardoublestar():
    ...

def test_allfuncs():
    ...