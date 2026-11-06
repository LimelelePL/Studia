from sentence_utils import (
    advance_to_next_word,
    get_next_word,
    read_sentece,
    run_main,
)


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
        # zachowanie struktury akapitow
        if not stripped:
            text += sentence
        elif count_connectors(sentence) >= 2:
            text += sentence

        sentence = read_sentece()

    return text


def main() -> None:
    print(sentences_with_two_connectors(), end="")


if __name__ == "__main__":
    run_main(main)
