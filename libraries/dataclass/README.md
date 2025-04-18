# [`dataclass`](https://docs.python.org/3/library/dataclasses.html)

The `dataclasses` module in Python (introduced in **Python 3.7**) provides a decorator and functions for **automatically adding special methods** like `__init__`, `__repr__`, `__eq__`, and more to classes, **making your code cleaner and less repetitive**.

> Note: Type annotations are mandatory for a field to be treated as a part of the dataclass. It requires type annotations to know which variables should be considered as fields and generate methods like `__init__`, `__repr__`, etc.

## Why use `@dataclass`?

Without `dataclass`:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

With `dataclass`:

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
```

That’s it! It handles `__init__`, `__repr__`, `__eq__`, etc. automatically.

## Basic Example

```python
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    pages: int

b = Book("1984", "George Orwell", 328)
print(b)  # Book(title='1984', author='George Orwell', pages=328)
```

## Features of `dataclass`

### 1. **Default Values**

```python
@dataclass
class Car:
    make: str
    model: str
    year: int = 2023

c = Car("Toyota", "Camry")
print(c.year)  # 2023
```

### 2. **Post-init Processing**

Is a special method in a dataclass that gets called automatically after the generated `__init__` method finishes.

It's useful when:
-You need to compute or validate additional values
-You want to modify fields based on others
-You want to run some custom logic after initialization

```python
@dataclass
class Product:
    name: str
    price: float

    def __post_init__(self):
        self.price_with_tax = self.price * 1.18

p = Product("Mouse", 500)
print(p.price_with_tax)  # 590.0
```

```python
class Rectangle:
    def __init__(self, width, length):
        self.width = width
        self.length = length

@dataclass
class Square(Rectangle):
    side: float

    def __post__init__(self):
        super().__init__(self.side, self.side)
```

### 3. **Comparison Methods**

```python
@dataclass
class Point:
    x: int
    y: int

p1 = Point(2, 3)
p2 = Point(2, 3)

print(p1 == p2)  # True (because __eq__ is auto-generated)
```

### 4. **Frozen Dataclasses** (immutable like `namedtuple`)

```python
@dataclass(frozen=True)
class Coordinates:
    lat: float
    lon: float

c = Coordinates(12.97, 77.59)
# c.lat = 13.00 will raise FrozenInstanceError
```

### 5. **`field()` for more control**

Consider this scenario where we assign a list(mutable data structure) as default parameter:

```python
def test_func(l=[]):
    l.append(1)
    print(l)

test_func() # Output: [1]
test_func() # Output: [1, 1]
```

You will similar behavior when list is defined as default value. To overcome this, we can use `field` with `default_factory` parameter from dataclass. Mutable default values (like lists, dicts, sets) should not be passed directly as default because all instances of the class will share the same list, leading to unexpected behavior.

```python
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    grades: list = field(default_factory=list)

s = Student("Alice")
s.grades.append(90)
print(s.grades)  # [90]
```

### 6. **Define Class Variable**

In a dataclass, if you want to define a **_class variable_** (i.e., a variable shared by all instances and not included in `__init__`, `__repr__`, or equality comparisons), you need to use `typing.ClassVar`.

```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Dog:
    name: str
    age: int
    species: ClassVar[str] = "Canine"

d1 = Dog("Buddy", 3)
d2 = Dog("Charlie", 5)

print(d1)           # Dog(name='Buddy', age=3)
print(Dog.species)  # Canine
```

`species` is a class variable and will not appear in `__init__` or `repr`, because it's not treated as a dataclass field.

### 7. **Inheritance**

```python
@dataclass
class Rectangle:
    width: float
    length: float

@dataclass
class ColoredRectangle(Rectangle):
    color: str

rect = ColoredRectangle(11, 15, "Green") # follow the reverse method resolution
```

### 8. **`InitVar`**

`InitVar` (short for **Initialization Variable**) is used when:

- You want to **pass a value during initialization**,
- But **you don't want to store it as a regular field** in the dataclass.

It's mostly useful with `__post_init__`.

> “Think of it as I need this value **only during initialization**, not as part of the class instance.”

**_Why use `InitVar`?_**

- Cleanly separates **inputs** from **stored state**.
- Helps with **one-time computations** or validations.
- Reduces memory footprint by not storing unnecessary data.

```python
from dataclasses import dataclass, field, InitVar

@dataclass
class Student:
    name: str
    marks: InitVar[int]  # Used only during init
    grade: str = field(init=False)  # Will be set in post_init

    def __post_init__(self, marks):
        self.grade = "A" if marks >= 90 else "B"

s = Student("Alice", 92)
print(s.name)    # Alice
print(s.grade)   # A
# print(s.marks) AttributeError: 'Student' object has no attribute 'marks'
```

`marks` is:

- Passed during initialization
- Used in `__post_init__()`
- Not saved as an instance attribute

```python
#  Hashing Password During Init
from dataclasses import dataclass, field, InitVar
import hashlib

@dataclass
class User:
    username: str
    plain_password: InitVar[str]
    password_hash: str = field(init=False)

    def __post_init__(self, plain_password):
        self.password_hash = hashlib.sha256(plain_password.encode()).hexdigest()

u = User("bob", "mysecret")
print(u.username)        # bob
print(u.password_hash)   # (hashed string)
```

Readings:

- [Python Data Classes Are AMAZING! Here's Why](https://www.youtube.com/watch?v=5mMpM8zK4pY)
