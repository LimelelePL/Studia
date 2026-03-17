import sys
from common import iter_sentences


def _is_conjunction(word: str) -> bool:
    w = word.lower()
    return w == "i" or w == "oraz" or w == "ale" or w == "że" or w == "lub"


def _conjunction_count(sentence: str) -> int:
    count = 0
    word = ""
    for ch in sentence:
        if ch.isalpha():
            word += ch
        elif word:
            if _is_conjunction(word):
                count += 1
            word = ""
    if word and _is_conjunction(word):
        count += 1
    return count


def filter_conjunctions(stream=None):
    if stream is None:
        stream = sys.stdin
    for item in iter_sentences(stream):
        if item == "":
            yield ""
        elif _conjunction_count(item) >= 2:
            yield item


if __name__ == "__main__":
    for sentence in filter_conjunctions():
        print(sentence)
