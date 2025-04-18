# Code Coverage in Python

## What is Code Coverage?

- **Definition**: Code coverage measures the extent to which source code is executed by a test suite.
- **Purpose**:
  - Identifies untested code paths.
  - Highlights weaknesses in test strategy.
  - Leads to more robust and reliable software.

## The [`coverage`](https://coverage.readthedocs.io/en/7.8.0/) Library

### Key Features

- Measures which lines of code are executed during tests.
- Supports:
  - **Line coverage**
  - **Branch coverage**
  - **Report formats**: text, HTML, XML, LCOV, JSON
- Can identify **which tests hit specific lines**.

### Basic Usage

**Example Code:**

_File: `src/my_module.py`_

```python
def greet(name):
    if name:
        return f"Hello, {name}!"
    else:
        return "Hello there!"
```

_Test File: `tests/test_my_module.py`_

```python
import unittest
from src.my_module import greet

class TestGreetFunction(unittest.TestCase):
    def test_greet_with_name(self):
        self.assertEqual(greet("World"), "Hello, World!")

    def test_greet_without_name(self):
        self.assertEqual(greet(None), "Hello there!")
```

_Steps:_

```bash
$ python3 -m pip install coverage
$ coverage run -m unittest discover tests
$ coverage report -m       # Shows report in terminal with missing lines
$ coverage html            # Generates HTML report in htmlcov/index.html
```

### Integration with Testing Frameworks

#### `unittest` Integration

- **Command**:
  ```bash
  $ coverage run -m unittest discover <test_directory>
  $ coverage report -m
  $ coverage html
  ```
- Discovers test files matching pattern like `test*.py`.
- Reports include:
  - Total statements
  - Missed lines
  - Line numbers missed
  - % coverage

#### `pytest` Integration (2 Ways)

1. **Using `coverage run`**:

   ```bash
   $ coverage run --source=src -m pytest tests/
   $ coverage report -m
   $ coverage html
   ```

2. **Using `pytest-cov` Plugin**:
   - Install:
     ```bash
     $ pip install pytest-cov
     ```
   - Commands:
     ```bash
     $ pytest --cov=src                   # Terminal report
     $ pytest --cov=src --cov-report=html:coverage_html
     ```

### Configuration with `.coveragerc`

Example settings:

```ini
[run]
branch = True
source = src

[report]
omit =
    tests/*
    */site-packages/*
```

- **Customize** what’s measured/excluded.
- Can exclude lines using `# pragma: no cover`.

### Comparison: `unittest` vs `pytest` with Coverage

| Feature            | `unittest` + coverage               | `pytest` + coverage      | `pytest` + `pytest-cov` |
| ------------------ | ----------------------------------- | ------------------------ | ----------------------- |
| Execution Command  | `coverage run -m unittest discover` | `coverage run -m pytest` | `pytest --cov=src`      |
| Plugin Needed      | No                                  | No                       | Yes (`pytest-cov`)      |
| Integrated Options | Mostly via coverage CLI             | Mostly via CLI           | Direct in pytest        |
| Report Generation  | Separate commands                   | Separate commands        | Via `--cov-report`      |
| Config Support     | `.coveragerc`                       | `.coveragerc`            | `.coveragerc`           |

### Advanced Features

#### Branch Coverage

- Tracks execution of **if/else** branches.
- Enable with:
  ```bash
  $ coverage run --branch -m pytest
  ```

#### Exclusions

- Line-level: `# pragma: no cover`
- File/Dir-level:
  ```bash
  $ coverage run --omit="tests/*"
  ```

#### CI/CD Integration

- Run coverage on every commit.
- Combine with tools like:
  - **Codecov**
  - **Coveralls**
- Benefits:
  - Continuous feedback
  - Track test coverage trends
  - Enforce quality gates

## Summary

- **Code coverage** helps ensure testing thoroughness but isn't the sole metric of test quality.
- Use `coverage.py` with `unittest` or `pytest` to measure test effectiveness.
- Prefer **`pytest-cov`** for tighter integration and report flexibility.
- Keep a `.coveragerc` file for consistent configuration.
- Aim for **meaningful** and **comprehensive** test coverage — not just high percentages.

Readings:

- [Notes](https://docs.google.com/document/d/1-Esg-tMBbQt0Ei4UINM3rJ1Xp2p1F1S1DxIWdYqqzVc/edit?usp=sharing)
