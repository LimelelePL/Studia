import sys
from common import iter_sentences


def _has_proper_noun(sentence: str) -> bool:
    word = ""
    is_first = True
    for ch in sentence:
        if ch.isalpha():
            word += ch
        elif word:
            if not is_first and word[0].isupper():
                return True
            is_first = False
            word = ""
    if word and not is_first and word[0].isupper():
        return True
    return False


def proper_nouns_pct(stream=None) -> float:
    if stream is None:
        stream = sys.stdin
    total = 0
    with_proper = 0
    for item in iter_sentences(stream):
        if item == "":
            continue
        total += 1
        if _has_proper_noun(item):
            with_proper += 1
    if total == 0:
        return 0.0
    return with_proper / total * 100


if __name__ == "__main__":
    print(f"{proper_nouns_pct():.2f}%")
