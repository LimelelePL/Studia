import sys


def count_chars(stream=None) -> int:
    if stream is None:
        stream = sys.stdin
    count = 0
    for raw in stream:
        for ch in raw:
            if not ch.isspace():
                count += 1
    return count


if __name__ == "__main__":
    print(count_chars())
