import os
from pathlib import Path


def parse_filters(args: list[str]) -> list[str]:
    return [arg for arg in args if arg]


# funkcje os.listdir(), Path.iterdir() – zwraca listę
# plików i katalogów w ścieżce
def walktree(top: Path, callback):
    try:
        for path in top.iterdir():
            if path.is_file():
                callback(path)
            elif path.is_dir():
                # walktree(path, callback)  # zakomentowane bo nie mamy tak gleboko zagladac
                pass
    except PermissionError:
        pass  # Ignorujemy błędy uprawnień


def visit_executable(file: Path):
    if os.access(str(file), os.X_OK):
        print(f"  [EXE] {file.name}")
