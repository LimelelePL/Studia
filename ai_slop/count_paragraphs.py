import sys


def count_paragraphs(stream=None) -> int:
    if stream is None:
        stream = sys.stdin
    count = 0
    in_para = False
    for raw in stream:
        line = raw.rstrip("\n")
        if line.strip():
            if not in_para:
                count += 1
                in_para = True
        else:
            in_para = False
    return count


if __name__ == "__main__":
    print(count_paragraphs())
