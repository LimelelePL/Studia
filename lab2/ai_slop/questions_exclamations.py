import sys
from common import iter_sentences


def filter_questions_exclamations(stream=None):
    if stream is None:
        stream = sys.stdin
    for item in iter_sentences(stream):
        if item == "":
            yield ""
        elif item[-1] in "?!":
            yield item


if __name__ == "__main__":
    for sentence in filter_questions_exclamations():
        print(sentence)
