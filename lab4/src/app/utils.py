import os
from pathlib import Path
from typing import Callable


def walktree(top: Path, callback: Callable[[Path], None]) -> None:
    try:
        for path in top.iterdir():
            if path.is_file():
                callback(path)
    except PermissionError:
        pass  # Ignorujemy b³êdy uprawnieñ


def visit_executable(file: Path) -> None:
    if os.access(str(file), os.X_OK):
        print(f"  [EXE] {file.name}")
