import os
import sys
from collections.abc import Callable
from pathlib import Path

from app.constants import PathMode


def get_path_variable() -> str | None:
    return os.environ.get("PATH")


def split_to_directories(path_variable: str | None) -> list[Path] | None:

    if not path_variable:
        return None

    return [Path(p) for p in path_variable.split(os.pathsep)]


def walktree(top: Path, callback: Callable[[Path], None]) -> None:
    try:
        for path in top.iterdir():
            if path.is_file():
                callback(path)
    except PermissionError:
        pass


def visit_executable(file: Path) -> None:
    if os.access(str(file), os.X_OK):
        print(f"  [EXE] {file.name}")


def print_executables(path_directories: list[Path] | None) -> None:

    arg = sys.argv[1].lower()

    if not path_directories:
        print("Brak ")
        return

    for directory in path_directories:
        if directory.is_dir():
            if arg == PathMode.ONLY_DIRS:
                print(f"\n {directory}")
            elif arg == PathMode.ALL:
                print(f"\n--- KATALOG: {directory} ---")
                walktree(directory, visit_executable)
            else:
                print("unknown parameter")
                break


if __name__ == "__main__":
    print_executables(split_to_directories(get_path_variable()))
