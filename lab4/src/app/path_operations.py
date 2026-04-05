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
    # ewentualnie gdy brak uprawien mozna by to wypisac
    if os.access(str(file), os.X_OK):
        print(f"  [EXE] {file.name}")


def print_executables(path_directories: list[Path] | None) -> None:
    # Trzeba określić zachowanie gdy nie podano żadnych argumentów lub więcej niż jeden, imo po prostu domyslne same
    # katalogi a gdy więcej niż jeden argument to ignorujemy reszte

    cli_args = PathMode.DIR if len(sys.argv) < 2 else sys.argv[1].casefold()

    if not path_directories:
        print("Brak danych w zmiennej środowiskowej PATH")
        return

    # Można by sie zastanowić czy nie lepiej tutaj zrobić 2 funkcje print_files print_dir czy cos
    for directory in path_directories:
        if directory.is_dir():
            if cli_args == PathMode.DIR:
                print(f"\n {directory}")
            elif cli_args == PathMode.ALL:
                print(f"\n--- KATALOG: {directory} ---")
                walktree(directory, visit_executable)
            else:
                print(
                    "Podano niepoprawny parametr, poprawne parametry: dir - lista katalogów, exe - lista katalogów i plików"  # noqa: E501
                )
                break


if __name__ == "__main__":
    print_executables(split_to_directories(get_path_variable()))
