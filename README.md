# pipe-iter

A package to allow chaining of functional operations on iterators.

## Motivation

## Usage

### Constructing an Iter

### Settings

#### Mutability

Many methods of `Iter` return an `Iter`. These methods typically do not consumer the underlying iterator but instead add further transformations to it. Whether this generates a new object or mutates the original object is controlled by the `and_mut` parameter in the initializer and constructor functions. The default (`and_mut=False`) is analogous to Python's built in iterator functions: each method returns a new object, which is distinct from but linked to the original iterator.

```python
itr1 = Iter(range(10))
itr2 = itr1.map(lambda x: x * 2, itr1)
print(next(itr1)) # 0
print(next(itr2)) # 2
print(next(itr1)) # 2
```

In contrast, for a mutable `Iter`, this:

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

The term `and_mut` is inspired by Rust: the idea is that the behavior of methods in a mutable Iter is analogous to a method with a signature of `(&mut self, ...)`. There is, as far as I know, no way to reproduce the behavior of an owned method call (`(self,...)`).

### Lazy Methods

### Consuming Operations
