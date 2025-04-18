# Development Tools

| Contents          |
| :---------------- |
| [Poetry](#poetry) |

## [Poetry](https://python-poetry.org/docs/)

Poetry is a tool for Python dependency management and packaging. It helps you declare, manage, and install dependencies in a consistent and reliable way, while also managing virtual environments and packaging configurations through a single interface.

### [Installation](https://python-poetry.org/docs/#installation)

| Operating System | Installation Method             | Command                                                                                                 |
| ---------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Windows          | Official Installer (PowerShell) | `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content`                   |
| Windows          | pipx                            | `pipx install poetry`                                                                                   |
| macOS            | Official Installer (Terminal)   | `curl -sSL https://install.python-poetry.org`                                                           |
| macOS            | pipx                            | `pipx install poetry`                                                                                   |
| macOS            | brew                            | `brew install poetry`                                                                                   |
| macOS            | MacPorts                        | `sudo port install poetry`                                                                              |
| Linux            | Official Installer (Terminal)   | `curl -sSL https://install.python-poetry.org`                                                           |
| Linux            | pipx                            | `pipx install poetry`                                                                                   |
| Linux            | Manual (pip + venv)             | `python3 -m venv <path>; source <path>/bin/activate; pip install -U pip setuptools; pip install poetry` |

### Create new Python projects using Poetry

Poetry simplifies the creation of new projects and manages virtual environments automatically.

To create a new project:

```bash
poetry new my_project
```

This generates a standard structure with the following:

```bash
my_project/
├── pyproject.toml
├── README.rst
├── my_project/
│   └── __init__.py
└── tests/
    └── __init__.py
```

To create a virtual environment and activate it:

```bash
cd my_project
poetry install
poetry shell  # activates the virtual environment
```

**Options:**

`--interactive`: guided setup

`--name`, `--flat`, `--description`, `--author`, `--python`, `--dependency`, `--dev-dependency`

Poetry automatically manages virtual environments in the background, so you don’t have to use `venv` or `virtualenv` manually.

### Configure your project with the `pyproject.toml` file

The `pyproject.toml` file is at the heart of any Poetry-managed project. It contains all configuration related to dependencies, project metadata, scripts, and build settings.

1. [build-system] (PEP 517)

```toml
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

2. [project] (PEP 621) Contains:

- `name`, `version`, `description`, `license`
- `requires-python`, `authors`, `keywords`, `urls`
- `dependencies`, `optional-dependencies`
- `scripts`, `entry-points`, `dynamic`

3. [tool.poetry]: Poetry-specific settings like:

- Dependency groups
- Package include/exclude
- Plugins and repository configs

Checkout [here](https://github.com/pypa/sampleproject/blob/main/pyproject.toml) for sample toml config file.

### Pinning Dependency Versions

**Version Specifiers:**

- `^1.2.3`: it means ≥1.2.3 and <2.0.0 (default)
- `~1.2.3`: it means ≥1.2.3 and <1.3.0
- `1.*`: any version in 1.x
- `>=1.2.0, <2.0.0`: inequality range
- `~=1.2.3`: compatible release

**Benefits:**

- Reproducible builds
- Avoids unexpected breaking changes
- Easier debugging

> Note: Use `poetry update` to refresh to latest versions within constraints.

### `poetry.lock` File

**Purpose:**

Records the exact versions of all direct and transitive dependencies used in the project. This guarantees consistency across different machines and environments.

**Auto-generated on:**

- `poetry install` (if the lock file doesn't exist)
- When you run `poetry add`, `poetry remove`, or `poetry update` to modify dependencies in `pyproject.toml`

**Usage:**

- Ensures consistent environments by locking dependency versions, preventing unexpected issues due to version changes.
- Speeds up installations since Poetry uses the locked versions directly instead of re-evaluating version constraints.

**_Best Practice: Always commit the poetry.lock file to version control to ensure all collaborators and deployments use the exact same dependencies._**

### Basic CLI Commands

| Command                        | Description                        |
| ------------------------------ | ---------------------------------- |
| `poetry new <name>`            | Create new project                 |
| `poetry init`                  | Initialize `pyproject.toml`        |
| `poetry add <pkg>`             | Add a dependency                   |
| `poetry add --group dev <pkg>` | Add a dev dependency               |
| `poetry remove <pkg>`          | Remove dependency                  |
| `poetry install`               | Install dependencies               |
| `poetry update [<pkg>]`        | Update dependencies                |
| `poetry run <cmd>`             | Run command in virtual environment |
| `poetry shell`                 | Start virtual environment shell    |
| `poetry lock`                  | Update `poetry.lock`               |
| `poetry build`                 | Build package (wheel/tar.gz)       |
| `poetry publish`               | Publish to PyPI                    |
| `poetry config`                | View/set configuration             |
| `poetry show`                  | List installed packages            |

### Adding Poetry to Existing Projects

1. Install Poetry (if not already).
2. Navigate to project root.
3. Run:
   ```bash
   poetry init
   ```
   - Fill in metadata
   - Skip dependency input if using requirements.txt
4. Convert dependencies:
   - Manually copy from requirements.txt
   - Or use:
     ```bash
     poetry add <package>
     ```
5. Install & generate lock file:
   ```bash
   poetry install
   ```
6. Enable in-project venv (optional):
   ```bash
   poetry config virtualenvs.in-project true
   ```

Readings:

- [Stop Wasting Hours - Every Python Dev NEEDS to Master Poetry](https://www.youtube.com/watch?v=nrm8Lre-x_8)
- [Python Poetry in 8 Minutes](https://www.youtube.com/watch?v=Ji2XDxmXSOM)