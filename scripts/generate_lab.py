import os
import sys
import subprocess

DEV_DEPENDENCIES = ["mypy", "pytest", "ruff"]
DEPENDENCIES = []

RUFF_CONFIG = """
[tool.ruff]
preview = true

[tool.ruff.lint]
select = [
    "E",      
    "F",     
    "I",      
    "B",      
    "UP",    
    "N",      
    "C4",     
    "RUF",    
]
"""
README_CONTENT = """
# Jężyki skryptowe

---

## Requirements

- [uv](https://docs.astral.sh/uv/)

---

## Run

Install dependencies:
```bash
uv sync
```

Run the script (example):
```bash
uv run <filename>.py
```

    """


def create_new_lab(directory: str, extra_deps: list[str]) -> None:
    if os.path.exists(directory):
        print(f"Error: Directory '{directory}' already exists.")
        sys.exit(1)

    os.makedirs(directory)
    print(f"Directory created: {directory}")

    subprocess.run(["uv", "init"], cwd=directory, check=True)

    if extra_deps:
        subprocess.run(
            ["uv", "add"] + extra_deps + DEPENDENCIES, cwd=directory, check=True
        )

    subprocess.run(["uv", "add", "--dev"] + DEV_DEPENDENCIES, cwd=directory, check=True)

    with open(os.path.join(directory, "pyproject.toml"), "a", encoding="utf-8") as f:
        f.write(RUFF_CONFIG)

    with open(os.path.join(directory, ".gitignore"), "a", encoding="utf-8") as f:
        f.write("\n.venv\n")
        f.write("\n__pycache__/\n")
        f.write("\n*.pyc\n")
    with open(os.path.join(directory, "README.md"), "w", encoding="utf-8") as f:
        f.write(README_CONTENT)

    print("Environment configured successfully.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python generate_lab.py <directory_name> [additional_dependencies]"
        )
        sys.exit(1)

    create_new_lab(sys.argv[1], sys.argv[2:])
