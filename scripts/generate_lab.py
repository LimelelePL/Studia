import os
import sys
import subprocess

DEV_DEPENDENCIES = ["mypy", "pytest", "ruff"]
DEPENDENCIES = []

PYPROJECT_TEMPLATE = """\
[project]
name = "{name}"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []

[project.scripts]
{name} = "app.main:main"

[tool.uv]
package = true

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/app"]

[dependency-groups]
dev = [
    "mypy>=1.0.0",
    "pytest>=9.0.0",
    "ruff>=0.15.0",
]

[tool.ruff]
preview = true
line-length = 120

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
    "N",    # pep8-naming
    "C4",   # flake8-comprehensions
    "RUF",  # ruff-specific
    "SIM",  # flake8-simplify
    "T20",  # flake8-print (no stray print())
    "PT",   # flake8-pytest-style
    "ERA",  # eradicate (no commented-out code)
    "S",    # flake8-bandit (security)
    "RET"   # flake8-return
]
ignore = [
    "S101",   # allow assert in tests
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S", "T20"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
strict = true
python_version = "3.13"

[tool.pytest.ini_options]
testpaths = ["tests"]
"""

MAIN_CONTENT = """\
def main() -> None:
    print("Hello from {name}!")


if __name__ == "__main__":
    main()
"""

INIT_CONTENT = """\
"""

README_CONTENT = """\
# {name}

---

## Requirements

- [uv](https://docs.astral.sh/uv/)

---

## Run

Install dependencies:
```bash
uv sync
```

Run the script:
```bash
uv run {name}
```
"""

GITIGNORE_CONTENT = """\
.venv/
__pycache__/
*.pyc
*.pyo
.mypy_cache/
.ruff_cache/
.pytest_cache/
dist/
*.egg-info/
"""


def create_new_lab(directory: str, extra_deps: list[str]) -> None:
    if os.path.exists(directory):
        print(f"Error: Directory '{directory}' already exists.")
        sys.exit(1)

    # Struktura katalogów
    src_app = os.path.join(directory, "src", "app")
    tests_dir = os.path.join(directory, "tests")
    os.makedirs(src_app)
    os.makedirs(tests_dir)
    print(f"Directory structure created: {directory}/")

    # src/app/main.py i __init__.py
    with open(os.path.join(src_app, "main.py"), "w", encoding="utf-8") as f:
        f.write(MAIN_CONTENT.format(name=directory))

    with open(os.path.join(src_app, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(INIT_CONTENT)

    # tests/__init__.py
    with open(os.path.join(tests_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("")

    # pyproject.toml – pełny szablon zamiast dopisywania
    with open(os.path.join(directory, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(PYPROJECT_TEMPLATE.format(name=directory))

    # .gitignore
    with open(os.path.join(directory, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(GITIGNORE_CONTENT)

    # README.md
    with open(os.path.join(directory, "README.md"), "w", encoding="utf-8") as f:
        f.write(README_CONTENT.format(name=directory))

    # Instalacja zależności przez uv
    if extra_deps:
        subprocess.run(
            ["uv", "add"] + extra_deps + DEPENDENCIES,
            cwd=directory,
            check=True,
        )

    subprocess.run(
        ["uv", "add", "--dev"] + DEV_DEPENDENCIES,
        cwd=directory,
        check=True,
    )

    print("Environment configured successfully.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python generate_lab.py <directory_name> [additional_dependencies]"
        )
        sys.exit(1)

    create_new_lab(sys.argv[1], sys.argv[2:])
