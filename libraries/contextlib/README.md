# [`contextlib`](https://docs.python.org/3/library/contextlib.html)

The `contextlib` library in Python is a **standard library module** that provides **utilities for working with context managers** — which are typically used with the `with` statement.

It's especially helpful when:

- You want to **write your own context manager** without defining a full class.
- You want to manage **resources** (like files, locks, etc.) neatly and safely.

## Why use `contextlib`?

Normally, context managers are used like this:

```python
with open("file.txt") as f:
    data = f.read()
```

But if you want to create your own custom context manager for something more specific — that’s where `contextlib` comes in handy.

## Common Tools in `contextlib`

### 1. `@contextmanager` — Turn a generator into a context manager

```python
from contextlib import contextmanager

@contextmanager
def open_file(name, mode):
    f = open(name, mode)
    try:
        yield f
    finally:
        f.close()

with open_file("example.txt", "w") as f:
    f.write("Hello, world!")
```

**How it works**:

- Code before `yield` runs when entering the context.
- Code after `yield` runs when exiting (even if there’s an exception).

### 2. `closing()` — Automatically close an object with a `.close()` method

Useful when an object needs to be cleaned up, but it doesn't support `with` by default.

```python
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen("https://example.com")) as page:
    print(page.read())
```

### 3. `suppress()` — Suppress specific exceptions

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    with open("nonexistent.txt") as f:
        data = f.read()
```

No error will be raised if the file is missing.

### 4. `redirect_stdout` and `redirect_stderr` — Redirect print output

```python
import sys
from contextlib import redirect_stdout

with open("output.txt", "w") as f:
    with redirect_stdout(f):
        print("This goes to the file instead of the console")
```

### 5. `nullcontext()` — Useful as a no-op context manager

```python
from contextlib import nullcontext

debug = False

with open("file.txt") if not debug else nullcontext() as f:
    if not debug:
        print(f.read())
    else:
        print("Debug mode - no file read")
```
