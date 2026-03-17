import sys


def iter_sentences(stream=None):
    """
    Yields sentences from stream.
    Sentence ends at .!? or at paragraph boundary (empty line).
    Yields empty string "" as paragraph boundary marker.
    """
    if stream is None:
        stream = sys.stdin

    sentence = ""
    prev_empty = False

    for raw in stream:
        line = raw.rstrip("\n")

        if not line.strip():
            if sentence.strip():
                yield sentence.strip()
                sentence = ""
            if not prev_empty:
                yield ""
            prev_empty = True
            continue

        prev_empty = False

        for ch in line:
            sentence += ch
            if ch in ".!?":
                trimmed = sentence.strip()
                if trimmed:
                    yield trimmed
                sentence = ""

        if sentence:
            sentence += " "

    if sentence.strip():
        yield sentence.strip()


def word_count(sentence: str) -> int:
    count = 0
    in_word = False
    for ch in sentence:
        if ch.isalpha():
            if not in_word:
                count += 1
                in_word = True
        else:
            in_word = False
    return count
