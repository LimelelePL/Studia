# wypisuje zdania zawierające co dwa wyrazy sposrod i oraz ale że lub
# Wypisuje tylko zdania zakończone ? albo !
import sys

from sentence_utils import advance_to_next_word, get_next_word, read_sentece

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")


def check_word(w: str) -> bool:
    return w == "i" or w == "oraz" or w == "ale" or w == "że" or w == "lub"


def count_connectors(sentence: str) -> int:
    count = 0
    rest = sentence

    while True:
        word = get_next_word(rest)
        if not word:
            break

        if check_word(word.lower()):
            count += 1

        rest = advance_to_next_word(rest)

    return count


def sentences_with_two_connectors() -> str:
    text = ""
    sentence = read_sentece()

    while sentence:
        stripped = sentence.rstrip()
        # zachowanie struktyy akapitow
        if not stripped:
            text += sentence
        if count_connectors(sentence) == 2:
            text += sentence

        sentence = read_sentece()

    return text


if __name__ == "__main__":
    print(sentences_with_two_connectors(), end="")
