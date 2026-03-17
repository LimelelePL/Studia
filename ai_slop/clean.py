import sys


def _normalize_line(line: str) -> str:
    result = ""
    prev_space = True
    for ch in line:
        if ch in " \t":
            if not prev_space:
                result += " "
            prev_space = True
        else:
            result += ch
            prev_space = False
    return result.rstrip()


def _preamble_end(lines: list) -> int:
    prev_empty = False
    for i, line in enumerate(lines):
        if line.strip() == "":
            if prev_empty:
                return i
            prev_empty = True
        else:
            prev_empty = False
    return -1


def iter_content(stream=None):
    if stream is None:
        stream = sys.stdin

    first_lines = []
    for raw in stream:
        first_lines.append(raw.rstrip("\n"))
        if len(first_lines) >= 10:
            break

    end = _preamble_end(first_lines)
    start = end + 1 if end >= 0 else 0

    for line in first_lines[start:]:
        if line.strip() == "-----":
            return
        yield _normalize_line(line)

    for raw in stream:
        line = raw.rstrip("\n")
        if line.strip() == "-----":
            return
        yield _normalize_line(line)


if __name__ == "__main__":
    for line in iter_content():
        print(line)
