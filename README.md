# Języki skryptowe

chuj pizda rama.

---

## Requirements

- [uv](https://docs.astral.sh/uv/) (Fast Python package and project manager)

---

## Workspace Setup & Generator

Instead of manually configuring each task folder, use the included `generate_lab.py` script. It automatically initializes a `uv` project, sets up dependencies (`mypy`, `pytest`, `ruff`), appends strict linting rules, and ignores the virtual environment.

### Generate lab directory

````bash
python ./scripts/generate_lab.py <directory_name> [additional_dependencies]
---

- [uv](https://docs.astral.sh/uv/)

---

```bash
git clone <repo>
cd <repo>
uv sync
````

## Run

```bash
uv run main.py
```

---

## Tools

### Ruff

Linter i formatter kodu. Łapie błędy, unused imports, złe praktyki i formatuje kod.

```bash
uv run ruff check .       # sprawdza błędy
uv run ruff check . --fix # sprawdza błędy i naprawia automatycznie
uv run ruff format .      # formatuje kod
```

### Mypy

Sprawdza poprawność typów.

```bash
uv run mypy .
```

---

## uv

```bash
uv add <pakiet>            # dodaje pakiet
uv add <pakiet> --dev      # dodaje pakiet tylko na development
uv remove <pakiet>         # usuwa pakiet
uv sync                    # instaluje wszystkie zależności z uv.lock
uv run <komenda>           # uruchomia komendę w środowisku projektu
```
