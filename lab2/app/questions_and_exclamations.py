# Wypisuje tylko zdania zakończone ? albo !
from sentence_utils import read_sentece


def questions_and_exclamations() -> str:
    text = ""
    sentence = read_sentece()

    while sentence:
        stripped = sentence.rstrip()
        # zachowanie akapitow
        if not stripped:
            text += sentence
        elif stripped[-1] in "!?":
            text += sentence

        sentence = read_sentece()

    return text


if __name__ == "__main__":
    print(questions_and_exclamations())
