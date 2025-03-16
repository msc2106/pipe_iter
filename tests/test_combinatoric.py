from pipe_iter import Iter
from pytest import raises

def test_permutations():
    assert (
        Iter('ABCD')
            .permutations(2)
            .map(lambda tpl: ''.join(tpl))
            .collect(lambda itr: ' '.join(itr))
        == 'AB AC AD BA BC BD CA CB CD DA DB DC'
    )
    assert (
        Iter(range(3))
            .permutations()
            .collect(list) 
        == [(0,1,2), (0,2,1), (1,0,2), (1,2,0), (2,0,1), (2,1,0)]
    )

def test_product():
    assert (
        Iter('ABCD')
            .product('xy')
            .map(lambda tpl: ''.join(tpl))
            .collect(lambda itr: ' '.join(itr))
        == 'Ax Ay Bx By Cx Cy Dx Dy'
    )
    itr = iter(range(2))
    prod_2_3 = Iter(itr).product(repeat=3) # consumes the original iterator
    with raises(StopIteration):
        next(itr)
    assert prod_2_3.collect(list) == [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]