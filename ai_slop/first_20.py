import sys
from common import iter_sentences


def first_n(stream=None, n: int = 20):
    if stream is None:
        stream = sys.stdin
    count = 0
    for item in iter_sentences(stream):
        if item == "":
            yield ""
        else:
            if count >= n:
                return
            yield item
            count += 1


if __name__ == "__main__":
    for sentence in first_n():
        print(sentence)
