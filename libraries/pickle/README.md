# [`pickle`](https://docs.python.org/3/library/pickle.html)

The `pickle` library in Python is used for **serializing and deserializing Python objects**, meaning:

- **Pickling**: Converting a Python object into a byte stream.
- **Unpickling**: Reconstructing the object from the byte stream.

This is useful when you want to:

- Save an object (like a model, dict, list, etc.) to a file.
- Send it over a network.
- Store it temporarily and retrieve it later.

## Example 1: Pickling (Saving) an Object

```python
import pickle

data = {"name": "Alice", "age": 30, "languages": ["Python", "JavaScript"]}

with open("data.pkl", "wb") as f:
    pickle.dump(data, f)
```

- `"wb"`: Write in binary mode.
- `pickle.dump()` writes the object to file.

## Example 2: Unpickling (Loading) an Object

```python
import pickle

with open("data.pkl", "rb") as f:
    loaded_data = pickle.load(f)

print(loaded_data)
# Output: {'name': 'Alice', 'age': 30, 'languages': ['Python', 'JavaScript']}
```

## Example 3: Pickle to/from Bytes (not files)

```python
obj = [1, 2, 3, {"a": 100, "b": 200}]

# Serialize to bytes
pickled_bytes = pickle.dumps(obj)

# Deserialize from bytes
restored = pickle.loads(pickled_bytes)

print(restored)  # Output: [1, 2, 3, {'a': 100, 'b': 200}]
```

## Security Warning

> **Never unpickle data from an untrusted source.**

Pickle can execute arbitrary code and lead to serious security issues. If you're working with untrusted data, consider using **`json`** for serialization instead.

## Custom Objects with Pickle

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("Bob", 40)

# Save object
with open("person.pkl", "wb") as f:
    pickle.dump(p1, f)

# Load object
with open("person.pkl", "rb") as f:
    person_loaded = pickle.load(f)

print(person_loaded.name)  # Output: Bob
```

## Summary

| Function         | Use                    |
| ---------------- | ---------------------- |
| `pickle.dump()`  | Serialize to file      |
| `pickle.load()`  | Deserialize from file  |
| `pickle.dumps()` | Serialize to bytes     |
| `pickle.loads()` | Deserialize from bytes |
