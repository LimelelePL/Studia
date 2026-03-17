import sys
from common import iter_sentences


def _comma_count(sentence: str) -> int:
    count = 0
    for ch in sentence:
        if ch == ",":
            count += 1
    return count


def first_with_subordinate(stream=None) -> str:
    if stream is None:
        stream = sys.stdin
    for item in iter_sentences(stream):
        if item != "" and _comma_count(item) >= 2:
            return item
    return ""


if __name__ == "__main__":
    result = first_with_subordinate()
    if result:
        print(result)
