import sys
from common import iter_sentences


def longest_sentence(stream=None) -> str:
    if stream is None:
        stream = sys.stdin
    longest = ""
    for item in iter_sentences(stream):
        if item != "" and len(item) > len(longest):
            longest = item
    return longest


if __name__ == "__main__":
    result = longest_sentence()
    if result:
        print(result)
