# Development Tools

| Contents          |
| :---------------- |
| [Poetry](#poetry) |
| [UV](#uv)         |

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

## [UV](https://docs.astral.sh/uv/)

- UV is an extremely fast Python package and project manager, written in Rust by Astral (the creators of the linter Ruff)
- It consolidates many tools into one: it can replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more
  - `pip` → for installing packages
  - `venv / virtualenv` → for virtual environment creation/management
  - `pip-tools` → for lock files and reproducible environments
  - `pipx` → for installing & running Python-based CLI tools globally
- Performance is a standout: 10–100× faster than pip, especially when using a warm cache; up to 115× faster in some benchmarks
- Supports dependency management, virtual environments, Python version management, script execution, tool invocation, lockfiles, workspaces, and publishing workflows
- Works across macOS, Linux, and Windows

### [Installation](https://docs.astral.sh/uv/getting-started/installation/)

You can install uv in multiple ways:

1. **Standalone installer (recommended):**

   - On macOs/Linux:

     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```

   - On Windows (PowerShell):

      ```bash
      powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
      ```

2. **Via PyPI or pipx:**

   ```bash
   pip install uv
   pipx install uv
   ```

3. **Homebrew or Pacman (on macOS and Linux)**

   ```bash
   brew install uv
   pacman -S uv
   ```

4. If installed via standalone, you can update itself via:

   ```bash
   uv self update
   ```

### [Create New Python Projects Using UV](https://docs.astral.sh/uv/concepts/projects/init/)

Instead of manually creating dirs, virtual environments, and requirements files, UV automates everything.

1. **Initialize a project (default: app):**

   ```bash
   uv init my_project
   ```

   This generates:

   - `.git/` + `.gitignore` (Git repo initialized)
   - `.python-version` (ensures consistent Python version)
   - `pyproject.toml` (modern dependency management)
   - `README.md` (empty template)
   - `main.py` (starter file)

2. **Project types:**

   - `app` → (default) for applications, scripts, web servers
   - `lib` → for libraries meant to be distributed as Python packages

     usage:

     ```bash
     uv init my_project --app
     # OR
     uv init my_project --lib
     ```

3. **Adding dependencies:**

   ```bash
   uv add flask requests
   ```

   - Creates a virtual environment automatically (no manual `venv` or `activate`)
   - Updates `pyproject.toml` and generates a `uv.lock` file

4. Running code (without activating env manually):

   ```bash
   uv run main.py
   ```

   UV ensures the right interpreter + dependencies are used.

### Add Existing Python Project to UV

If you already have a project (say with `requirements.txt`):

1. **Initialize with UV:**

   ```bash
   uv init
   ```

2. Import dependencies:

   ```bash
   uv add -r requirements.txt
   ```

3. UV converts them into `pyproject.toml` + `uv.lock`. At this point, `requirements.txt` can be removed since UV ensures reproducibility via the lock file.

### UV CLI Commands (Commonly Used)

#### Project & Dependencies

- `uv init [name]` → create a new project
- `uv add <pkg>` → add dependency (updates pyproject.toml & uv.lock)
- `uv remove <pkg>` → remove dependency
- `uv sync` → recreate env exactly from lock file
- `uv tree` → show dependency tree

#### Running Code

- `uv run script.py` → run code inside project env (no manual activation)

#### Virtual Environments

- No need for `python -m venv` or `source venv/bin/activate` → UV does it automatically.
- Even if `.venv` is deleted, `uv run` or `uv sync` recreates it instantly from lock file.

#### Compatibility with Pip

- `uv pip install <pkg>` → works like pip (good for gradual transition)
- `uv pip list` → list installed packages
- `uv pip freeze` → output dependencies like pip

(But note: using uv pip skips the lockfile benefits — best to switch to native uv add workflow.)

#### Tools (Pipx Replacement)

- Install a global CLI tool:

  ```bash
  uv tool install ruff
  ```

- Run a tool temporarily (without installing):

  ```bash
  uv tool run ruff check
  # or shorter alias
  uvx ruff check
  ```

- List tools:

  ```bash
  uv tool list
  ```

- Remove tool:

  ```bash
  uv tool uninstall ruff
  ```

- Upgrade tools:

  ```bash
  uv tool upgrade --all
  ```

Readings:

- [Python Tutorial: UV - A Faster, All-in-One Package Manager to Replace Pip and Venv](https://www.youtube.com/watch?v=AMdG7IjgSPM)
