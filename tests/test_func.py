from pipe_iter import star_func, doublestar_func, fallible_func, Iter
from pytest import raises

def test_doublestarfunc():
    ...

def test_doublestarfunc_invalid():
    ...

def test_falliblefunc():
    ...

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