import os
import sys
from pathlib import Path

from app.cosntants import zad2Constans
from app.utils import parse_filters, visit_executable, walktree


def get_path_variable() -> str | None:
    return os.environ.get("PATH")


def split_to_directories(path_variable: str | None):

    if not path_variable:
        return None

    return [Path(p) for p in path_variable.split(os.pathsep)]


def print_executables(path_directories: list[Path] | None):

    args = parse_filters(sys.argv[1:])
    if not args:
        print("Brak parametrów! Użyj all albo only_dirs .")
        return
    filter = args[0]

    if not path_directories:
        print("Brak ")
        return

    for directory in path_directories:
        if directory.is_dir():
            if filter == zad2Constans.ONLY_DIRS:
                print(f"\n {directory}")
            elif filter == zad2Constans.ALL:
                print(f"\n--- KATALOG: {directory} ---")
                walktree(directory, visit_executable)
            else:
                print("unknown parameter: ")
                break


if __name__ == "__main__":
    print_executables(split_to_directories(get_path_variable()))
