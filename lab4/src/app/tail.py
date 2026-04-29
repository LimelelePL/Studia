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


def print_file_tail(filename: Path, params: TailParams) -> None:
    tail_mode = os.environ.get("TAIL_MODE", "lines")
    tail_reverse = os.environ.get("TAIL_REVERSE", "") == "1"

    if tail_mode == "chars":
        size = os.stat(filename).st_size
        position = max(0, size - params.lines)
        with open(filename) as file:
            file.seek(position)
            content = file.read(params.lines)
        if tail_reverse:
            content = content[::-1]
        sys.stdout.write(content)
        sys.stdout.flush()
        return

    position = point_to_target(filename, params.lines)

    if not params.follow:
        with open(filename) as file:
            file.seek(position)
            lines = file.readlines()
        if tail_reverse:
            lines = list(reversed(lines))
        for line in lines:
            sys.stdout.write(line)
            sys.stdout.flush()
        return

    with open(filename) as file:
        file.seek(position)
        while True:
            line = file.readline()
            if line:
                sys.stdout.write(line)
                sys.stdout.flush()
            else:
                time.sleep(0.2)
                size = os.stat(filename).st_size
                if file.tell() > size:
                    sys.stdout.write("\n")
                    file.seek(point_to_target(filename, params.lines))


def print_stdin_tail(lines: int) -> None:
    tail_mode = os.environ.get("TAIL_MODE", "lines")
    tail_reverse = os.environ.get("TAIL_REVERSE", "") == "1"

    if tail_mode == "chars":
        buffer: deque[str] = deque(maxlen=max(0, lines))
        for char in sys.stdin.read():
            buffer.append(char)
        output = list(reversed(buffer)) if tail_reverse else list(buffer)
        sys.stdout.write("".join(output))
        sys.stdout.flush()
        return

    line_buffer: deque[str] = deque(maxlen=max(0, lines))
    for line in sys.stdin:
        line_buffer.append(line)
    output_lines = list(reversed(line_buffer)) if tail_reverse else list(line_buffer)
    for line in output_lines:
        sys.stdout.write(line)
        sys.stdout.flush()


def tail() -> None:
    params = parse_tail_arguments()
    stdin_has_data = not sys.stdin.isatty()

    if params.file_path:
        print_file_tail(params.file_path, params)
    elif stdin_has_data:
        if params.follow:
            print("Nie można użyc parametru --follow z poleceniem które przekazuje dane potokowo")
            return
        print_stdin_tail(params.lines)


if __name__ == "__main__":
    tail()
