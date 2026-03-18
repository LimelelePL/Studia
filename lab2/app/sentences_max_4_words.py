# Funkcja wypisująca tylko zdania zawierające co najwyżej 4 wyrazy.

from sentence_utils import advance_to_next_word, format_stream_utf8, read_sentece, skip_non_alpha


def count_words(sentence: str) -> int:
    count = 0
    sentence = skip_non_alpha(sentence)
    while sentence:
        count += 1
        sentence = advance_to_next_word(sentence)
    return count


def sentences_max_4_words() -> None:
    sentence = read_sentece()
    while sentence:
        if sentence.strip() and count_words(sentence) <= 4:
            print(sentence.strip())
        sentence = read_sentece()


if __name__ == "__main__":
    import sys
    format_stream_utf8()
    try:
        sentences_max_4_words()
    except BrokenPipeError:
        sys.exit(0)
