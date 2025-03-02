from collections.abc import Iterable, Iterator
from pipe_iter import Iter

def test_exhaustion():
    x = range(5)
    itr = Iter(x)
    first_run = ",".join(str(i) for i in itr)
    assert first_run == "0,1,2,3,4"
    second_run = ",".join(str(i) for i in itr)
    assert second_run == ""

def test_nocopy():
    x = range(5)
    itr1 = Iter(x)
    lst1 = [next(itr1)]
    itr2 = Iter(itr1)
    lst1.extend(list(itr1))
    lst2 = list(itr2)
    assert lst1 == list(x)
    assert lst2 == []

def test_mutability():
    x = range(5)
    immutable_iter = Iter(x)
    mutable_iter = Iter.and_mut(x)
    immut_map = immutable_iter.map(lambda x: x+1)
    mut_map = mutable_iter.map(lambda x: x+1)
    v1_immut = next(immutable_iter)
    v1_mut = next(mutable_iter)
    v2_immut = next(immut_map)
    v2_mut = next(mut_map)
    assert v1_immut == 0
    assert v1_mut == 1
    assert v2_immut == v2_mut == 2
    assert mutable_iter is mut_map
    assert immutable_iter is not immut_map

def test_link_to_source():
    x = list(range(5))
    lst1 = list(Iter(x))
    itr = Iter(x)
    assert x == lst1
    x[0] = -1
    x.append(5)
    assert x != lst1
    lst2 = list(itr)
    assert lst2 == x

def test_for():
    x = range(5)
    lst = []
    for i in Iter(x):
        lst.append(i)
    assert lst == list(x)

def test_lazy_eval():
    x = range(10)
    counter = 0
    def foo(x):
        nonlocal counter
        counter += 1
        return x+100
    itr = Iter(map(foo, x))
    assert counter == 0
    itr.collect(list)
    assert counter == 10

def test_inheritance():
    x = Iter([])
    assert isinstance(x, Iterable)
    assert isinstance(x, Iterator)