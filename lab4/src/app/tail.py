import argparse
import os
import sys
import time
from collections import deque
from pathlib import Path

from app.constants import TailParams


def parse_tail_arguments() -> TailParams:
    parser = argparse.ArgumentParser()

    parser.add_argument("file_path", nargs="?", type=Path)
    parser.add_argument("--lines", type=int, default=10)
    parser.add_argument("--follow", action="store_true")

    args = parser.parse_args()
    return TailParams(lines=args.lines, file_path=args.file_path, follow=args.follow)


def get_lines_count(file: Path) -> int:
    count = 0
    with open(file) as f:
        f.seek(0)
        while True:
            if not f.readline():
                break
            count += 1
    return count


# zwraca pozycje wskaźnika w miejscu gdzie powinno się zacząć wypisywanie pliku
def point_to_target(filename: Path, lines: int) -> int:
    total = get_lines_count(filename)
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


# wedlug mnie to ma dzialac tak:
# - na poczatku ma wypisać n ostatnich lini
# - dopiszemy jakieś linie do końca pliku to je wypisuje niezależnie od tego ile ich dopisano
# - skrócono plik to wpisuje znowu końcowe n lini (wersja z wykladu wraca na poczatek i wypisuje caly plik od zera)


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

            time.sleep(0.2)
            if params.follow:
                size = os.stat(filename).st_size

                if file.tell() > size:
                    sys.stdout.write("\n")
                    file.seek(point_to_target(filename, params.lines))


# TRZEBA ZAIMPLEMENTOWAC FOLLOW DLA TEJ OPCJI ALE NIE WIEM JAK!!!!!!!!!!!
# nie da sie dynamicznie sprawdzac dlugosci pliku xd to chyba wyjebane w to?
def print_stdin_tail(lines: int) -> None:
    buffer: deque[str] = deque(maxlen=max(0, lines))
    for line in sys.stdin:
        buffer.append(line)
    for line in buffer:
        time.sleep(0.2)
        sys.stdout.write(line)
        sys.stdout.flush()


def tail() -> None:
    params = parse_tail_arguments()
    stdin_has_data = not sys.stdin.isatty()

    if params.file_path:
        print_file_tail(params.file_path, params)
    elif stdin_has_data:
        print_stdin_tail(params.lines)


if __name__ == "__main__":
    tail()
