import sys
from common import iter_sentences, word_count


def filter_short(stream=None, max_words: int = 4):
    if stream is None:
        stream = sys.stdin
    for item in iter_sentences(stream):
        if item == "":
            yield ""
        elif word_count(item) <= max_words:
            yield item


if __name__ == "__main__":
    for sentence in filter_short():
        print(sentence)
