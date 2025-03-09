from pipe_iter import Iter
from pytest import raises

def test_accumulate():
    assert Iter([1, 2, 3, 4, 5]).accumulate().collect(list) == [1, 3, 6, 10, 15]
    assert Iter([1, 2, 3, 4, 5]).accumulate(initial=100).collect(list) == [100, 101, 103, 106, 110, 115]
    assert Iter([1, 2, 3, 4, 5]).accumulate(lambda a, b: a*b).collect(list) == [1, 2, 6, 24, 120]

def test_apply():
    def map_plus_one(iterator):
        return map(lambda x: x+1, iterator)
    assert Iter([1, 2, 3, 4, 5]).apply(map_plus_one).collect(list) == [2, 3, 4, 5, 6]

def test_batched():
    lst = list(range(8))
    batch_3_nofill = [(0, 1, 2), (3, 4, 5), (6, 7)]
    batch_3_nonefille = [(0, 1, 2), (3, 4, 5), (6, 7, None)]
    assert Iter(lst).batched(3).collect(list) == batch_3_nofill
    assert Iter(lst).batched(3, fillvalue=None).collect(list) == batch_3_nonefille
    with raises(TypeError):
        Iter(lst).batched(0, None).collect(list)

def test_chain():
    lst1 = ['a', 'b', 'c']
    lst2 = [1, 2, 3]
    assert Iter(lst1).chain(lst2).collect(list) == lst1 + lst2

def test_combinations():
    assert Iter('ABCD').combinations(2).map(lambda tpl: ''.join(tpl)).collect(set) == {'AB', 'AC', 'AD', 'BC', 'BD', 'CD'}
    assert Iter(range(4)).combinations(3).collect(set) == {(0,1,2), (0,1,3), (0,2,3), (1,2,3)}

def test_combinations_with_replacement():
    assert Iter('ABC').combinations_with_replacement(2).map(lambda tpl: ''.join(tpl)).collect(set) == {'AA', 'AB', 'AC', 'BB', 'BC', 'CC',}

def test_compress():
    assert Iter('ABCDEF').compress([1,0,1,0,1,1]).collect(lambda t: " ".join(t)) == "A C E F"

def test_cycle():
    n = 3
    N = 100
    itr = Iter(range(n)).cycle()
    for i, val in zip(range(N), itr):
        assert val == i % n

def test_dropwhile():
    assert Iter([1,4,6,3,8]).dropwhile(lambda x: x<5).collect(list) == [6, 3, 8]

def test_enumerate():
    assert Iter('ABC').enumerate().collect(list) == [(0, 'A'), (1, 'B'), (2, 'C')]
    assert Iter('ABC').enumerate(10).collect(list) == [(10, 'A'), (11, 'B'), (12, 'C')]

def test_evenitems():
    assert Iter(range(1,7)).evenitems().collect(list) == [2, 4, 6]

def test_filter():
    lst = list(range(5))
    odd = Iter(lst).filter(lambda x: x % 2).collect(list)
    assert odd == [1, 3]
    nonzero = Iter(lst).filter(None).collect(list)
    assert nonzero == [1, 2, 3, 4]
    nonzero = Iter(lst).fallible().filter(None).collect(list)
    assert nonzero == [1, 2, 3, 4]


def test_filterfalse():
    assert Iter([1,4,6,3,8]).filterfalse(lambda x: x<5).collect(list) == [6, 8]

def test_filter_map():
    d = {
        'a': 1,
        'c': 2,
        'e': 3,
    }
    itr = Iter("acbde").filter_map(lambda x: d.get(x, None))
    assert itr.collect(list) == [1, 2, 3]

def test_flat_map():
    assert Iter(range(3)).flat_map(lambda x: (x, -x)).collect(list) == [0, 0, 1, -1, 2, -2]
    with raises(TypeError):
        Iter(range(3)).flat_map(lambda x: -x).collect(list)

def test_flatten():
    # Reduces one level of nesting
    assert Iter([[0, 1], [2, 2]]).flatten().collect(list) == [0, 1, 2, 2]
    with raises(TypeError):
        Iter([[0, 1], 0, [2, 2]]).flatten().collect_args(print)

# def test_fork():
#     ...

def test_groupby():
    assert (
        Iter('AAAABBBCCDAABBB')
            .groupby()
            .map(lambda val: val[0])
            .collect(list)
        == ['A', 'B', "C", "D", "A", "B"]
    )
    assert (
        Iter('AAAABBBCCD')
            .groupby()
            .map(lambda val: ''.join(val[1]))
            .collect(list)
        == ['AAAA', 'BBB', "CC", "D"]
    )
    
    assert (
        Iter(range(9))
            .groupby(lambda x: x // 3)
            .star()
            .map(lambda g, val: [g, list(val)])
            .collect(list)
        == [[0, [0,1,2]], [1,[3,4,5]], [2,[6,7,8]]]
    )

def test_inspect():
    from math import sqrt
    collector = []
    def inspect_fn(val):
        collector.append(val)
    lst1 = Iter(range(5)).inspect(inspect_fn).collect(list)
    assert lst1 == collector == [0, 1, 2, 3, 4]

    collector2 = []
    def append_sqrt(val):
        collector2.append(sqrt(val))
    lst2 = Iter([-1, 0, 4]).fallible().inspect(append_sqrt).collect(list)
    assert collector2 == [0, 2.0]
    assert lst2 == [-1, 0, 4]

    with raises(ValueError):
        Iter([-1, 0, 4]).inspect(append_sqrt).collect(list)

def test_islice():
    ...

def test_map():
    ...

def test_odditems():
    ...

def test_pairwise():
    ...

def test_plus():
    ...

def test_product():
    ...

def test_permutations():
    ...

def test_skip():
    ...

def test_somevalue():
    x = [0, 1, None, 2, "", 3, None]
    assert Iter(x).somevalue().collect(list) == [0, 1, 2, "", 3]

def test_starmap():
    ...

def test_starmap_ignore_star_settings():
    ...

def test_stretch():
    # Selective and/or recursive flatten
    ...

def test_switch_map():
    ...

def test_takewhile():
    ...

def test_tee():
    ...

def test_zip_longest():
    ...