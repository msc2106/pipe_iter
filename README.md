# pipe-iter

A package to allow chaining of functional operations on iterators.

## Motivation

## Usage

### Initializing an Iter

### Lazy Methods

While these methods do not consume the iterator, they do mutate the `Iter` object. Thus, this:

```python
itr = Iter(range(10))
itr.map(str, itr)
print(*itr)
```

is equivalent to this:

```python
itr = Iter(range(10))
print(*itr.map(str, itr))
```

This is strictly speaking different from Python's built-in iteration functions, but it removes potential confusion arising from the fact that the input and output iterators of a function like `map` remain linked:

```python
itr1 = iter(range(10))
itr2 = map(lambda x: x * 2, itr1)
print(next(itr1)) # 0
print(next(itr2)) # 2
print(next(itr1)) # 2
```

This is different in implementation from Rust's iterators, which return new instances of distinct types, but similar in spirit, since the methods take ownership of the instance. If the outcome of two linked iterators is desired, the `mirror` method can be used.

### Consuming Operations
