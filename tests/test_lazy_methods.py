from pipe_iter import Iter

def test_accumulate():
    assert Iter([1, 2, 3, 4, 5]).accumulate().collect(list) == [1, 3, 6, 10, 15]
    assert Iter([1, 2, 3, 4, 5]).accumulate(initial=100).collect(list) == [100, 101, 103, 106, 110, 115]
    assert Iter([1, 2, 3, 4, 5]).accumulate(lambda a, b: a*b).collect(list) == [1, 2, 6, 24, 120]

def test_apply():
    def map_plus_one(iterator):
        return map(lambda x: x+1, iterator)
    assert Iter([1, 2, 3, 4, 5]).apply(map_plus_one).collect(list) == [2, 3, 4, 5, 6]

def test_batched():
    ...

def test_chain():
    # Appends another iterator
    ...

def test_combinations():
    ...

def test_combinations_with_replacement():
    ...

def test_compress():
    ...

def test_cycle():
    ...

def test_dropwhile():
    ...

def test_enumerate():
    ...

def test_evenitems():
    ...

def test_filter():
    ...

def test_filterfalse():
    ...

def test_filter_map():
    ...

def test_flat_map():
    ...

def test_flatten():
    # Reduces one level of nesting
    ...

def test_fork():
    ...

def test_group_by():
    ...

def test_inspect():
    ...

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