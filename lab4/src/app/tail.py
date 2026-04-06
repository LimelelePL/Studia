import argparse
import os
import sys
import time
from collections import deque
from pathlib import Path

from app.constants import TailParams


def parse_tail_arguments() -> TailParams:
    parser = argparse.ArgumentParser()

    parser.add_argument("file_path", type=Path)
    parser.add_argument("--lines", type=int, default=10)
    parser.add_argument("--follow", action="store_true")

    args = parser.parse_args()
    return TailParams(lines=args.lines, file_path=args.file_path, follow=args.follow)


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
            if not params.follow:
                break
            time.sleep(0.5)
            size = os.stat(filename).st_size

            # jezeli plik zostal nadpisany to ponownie wypisujemy n lini
            if file.tell() > size:
                file.seek(point_to_target(filename, params.lines))


# mega smart posuniecie ze strony koleig z ameryki
def print_stdin_tail(lines: int) -> None:
    buffer: deque[str] = deque(maxlen=max(0, lines))
    for line in sys.stdin:
        buffer.append(line)
    for line in buffer:
        sys.stdout.write(line)
        sys.stdout.flush()


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
