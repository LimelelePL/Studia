import re
from pathlib import Path

from app.constants import MEASUREMENTS_PATH


def group_measurement_files_by_key(directory: Path) -> dict[tuple[str, str, str], Path]:
    if not directory.is_dir():
        raise NotADirectoryError("podana ścieżka nie jest katalogiem! ")

    pattern = re.compile(r".*(\d{4})_([\w()]+)_([a-z0-9]+)\.csv$")

    result = {}
    for file in directory.iterdir():
        if file.is_file() and (match := pattern.search(str(file))):
            groups = match.groups()
            result[groups] = file

    return result


if __name__ == "__main__":
    print(group_measurement_files_by_key(MEASUREMENTS_PATH))
