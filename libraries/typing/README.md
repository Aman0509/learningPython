# [`typing`](https://docs.python.org/3/library/typing.html) module in Python

The typing module in Python provides support for **_type hints_**, which are **_annotations_** that indicate the expected data types of variables, function arguments, and return values. It helps developers write clearer, more maintainable, and bug-free code by making type expectations explicit.

In short, this module helps to document your code.

**Purpose of the typing module**

- **Code Clarity and Readability**: Type hints make code easier to understand for developers by specifying the types of inputs and outputs.
- **Error Detection**: Helps catch type-related bugs early, often during development, with tools like linters (e.g., `mypy`).
- **Better IDE Support**: Enables features like autocompletion and static type checking in Integrated Development Environments (IDEs).
- **Facilitates Collaboration**: Makes it easier for teams to work together by documenting the expected types in the code itself.

> Note: Type hints implemented via this module do not raise runtime exceptions if a variable is assigned a different type. They are purely informational and are meant to help with static type checking. Python remains a dynamically-typed language, meaning that it does not enforce types at runtime.

**How Type Hints Work**

- Type hints are annotations, and Python's interpreter ignores them during execution.
- They are used primarily by static type checkers like `mypy`, IDEs, or linters to catch type-related issues before runtime.

Example:

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

# This will run without any errors, despite `123` being an integer
print(greet(123))  # Output: Hello, 123
```

**Catching Type Errors with a Static Checker**

You can use tools like `mypy` to check for type violations:

- Install `mypy`

  ```bash
  pip install mypy
  ```

- Run `mypy` on your script: Save the code in a file, e.g., `example.py`, and run:

  ```bash
  mypy example.py
  ```

  ```
  # Output
  example.py:5: error: Argument 1 to "greet" has incompatible type "int"; expected "str"
  ```

## How to use Annotations?

1. **Variable Annotation**

   ```python
   x: int = 10  # `x` is expected to be an integer
   y: str = "Hello"  # `y` is expected to be a string
   ```

2. **Function Annotation**

   ```python
   def greet(name: str) -> str:
       return f"Hello, {name}"
   ```

3. **List Type**

   ```python
   from typing import List

   numbers: List[int] = [1, 2, 3, 4]  # A list of integers
   names: List[str] = ["Alice", "Bob", "Charlie"]  # A list of strings
   ```

4. **Tuple Type**

   ```python
   from typing import Tuple

   point: Tuple[int, int] = (3, 4)  # A tuple of two integers
   user: Tuple[str, int] = ("Alice", 25)  # A tuple of a string and an integer
   ```

5. **Dict Type**

   ```python
   from typing import Dict

   user_ages: Dict[str, int] = {"Alice": 25, "Bob": 30}  # Dictionary with string keys and integer values
   ```

6. **Set Type**

   ```python
   from typing import Set

   unique_numbers: Set[int] = {1, 2, 3}  # A set of integers
   unique_names: Set[str] = {"Alice", "Bob"}  # A set of strings
   ```

7. **Custom Type**

   ```python
   from typing import NewType

   UserId = NewType('UserId', int)  # Creating a custom type for user IDs

   def get_user_name(user_id: UserId) -> str:
       return f"User-{user_id}"

   user_id: UserId = UserId(100)
   print(get_user_name(user_id))  # Output: User-100
   ```

8. **Any Type**

   ```python
   from typing import Any

   data: Any = "Hello"  # Can be any type
   data = 123           # Valid
   data = [1, 2, 3]     # Also valid
   ```

9. **Optional Type**

   ```python
   from typing import Optional

   def find_user(user_id: int) -> Optional[str]:
       if user_id == 1:
           return "Alice"
       return None

   user = find_user(2)  # user can be either a string or None
   ```

10. **Sequence Type**

    ```python
    from typing import Sequence

    def print_items(items: Sequence[int]) -> None:
        for item in items:
            print(item)

    print_items([1, 2, 3])  # Works with a list
    print_items((4, 5, 6))  # Works with a tuple
    ```

11. **Callable Type**

    ```python
    from typing import Callable

    def execute(func: Callable[[int, int], int], a: int, b: int) -> int:
        return func(a, b)

    result = execute(lambda x, y: x + y, 5, 10)  # 15
    print(result)
    ```

12. **Generics Type**

    ```python
    from typing import List, TypeVar

    T = TypeVar('T')

    def get_first_item(items: List[T]) -> T:
        return items[0]
    ```

Readings:

- [Python Typing Module Tutorial: Use Cases and Code Snippets](https://www.squash.io/python-typing-module-tutorial-use-cases-and-code-snippets/)
- [Python Typing - Type Hints & Annotations](https://www.youtube.com/watch?v=QORvB-_mbZ0)
- [Python 3.12 Generic Types Explained](https://www.youtube.com/watch?v=q6ujWWaRdbA)
