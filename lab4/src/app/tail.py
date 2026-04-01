import os
import sys
import time
from collections import deque
from pathlib import Path

try:
    from app.constants import TailParams
except ModuleNotFoundError:
    from constants import TailParams


def parse_tail_arguments() -> TailParams:
    lines = 10
    file_path = None
    follow = False

    for arg in sys.argv[1:]:
        if arg.startswith("--lines="):
            try:
                value = int(arg.split("=", 1)[1])
            except (ValueError, IndexError):
                continue
            lines = max(0, value)
        elif arg == "--follow":
            follow = True
        elif not arg.startswith("--") and file_path is None:
            file_path = Path(arg)

    return TailParams(lines=lines, file_path=file_path, follow=follow)


def get_file_length(file: Path) -> int:
    count = 0
    with open(file) as f:
        f.seek(0)
        while True:
            if not f.readline():
                break
            count += 1
    return count


def point_to_target(filename: Path, lines: int) -> int:
    total = get_file_length(filename)
    target_line = total - lines
    if target_line <= 0:
        return 0

    with open(filename) as f:
        f.seek(0)
        current_line = 0
        position = 0
        while current_line < target_line:
            if not f.readline():
                break
            position = f.tell()
            current_line += 1
    return position


def print_file_tail(filename: Path, params: TailParams) -> None:
    position = point_to_target(filename, params.lines)
    with open(filename) as file:
        file.seek(position)
        while True:
            line = file.readline()
            if line:
                sys.stdout.write(line)
                sys.stdout.flush()
                continue
            if not params.follow:
                break
            time.sleep(0.5)
            size = os.stat(filename).st_size

            # jezeli plik zostal nadpisany to ponownie wypisujemy n lini
            if file.tell() > size:
                file.seek(point_to_target(filename, params.lines))
                continue


# mega smart posuniecie ze strony koleig z ameryki
def print_stdin_tail(lines: int) -> None:
    buffer = deque(maxlen=max(0, lines))
    for line in sys.stdin:
        buffer.append(line)
    for line in buffer:
        print(line, end="", flush=True)


# todo kurwa nie wiem jak ktos usunie jakas linie z pliku to co ma sie dziac????
# na wykladzie w przykladowym wskaznik wraca na góre i wypisuje caly plik z góry
# ale tutaj nie wiem jak ma być. Wypisywać znowu n lini z dolu????
def tail() -> None:
    params = parse_tail_arguments()
    stdin_has_data = not sys.stdin.isatty()

    if params.file_path:
        print_file_tail(params.file_path, params)
    elif stdin_has_data:
        print_stdin_tail(params.lines)


if __name__ == "__main__":
    tail()
