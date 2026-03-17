import sys
from common import iter_sentences


def _no_adjacent_same_start(sentence: str) -> bool:
    word = ""
    prev_first = ""
    for ch in sentence:
        if ch.isalpha():
            word += ch
        elif word:
            first = word[0].lower()
            if first == prev_first:
                return False
            prev_first = first
            word = ""
    if word and word[0].lower() == prev_first:
        return False
    return True


def longest_no_adjacent(stream=None) -> str:
    if stream is None:
        stream = sys.stdin
    longest = ""
    for item in iter_sentences(stream):
        if item != "" and _no_adjacent_same_start(item) and len(item) > len(longest):
            longest = item
    return longest


if __name__ == "__main__":
    result = longest_no_adjacent()
    if result:
        print(result)
