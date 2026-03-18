# Wypisuje najdłuższe zdanie, w którym żadne dwa
# sąsiadujące słowa nie zaczynają się na tę samą literę.
from sentence_utils import read_sentece, run_main, skip_spaces, update_max





def check(sentence: str) -> bool:
    sentence = sentence.strip()
    rest = sentence
    prev_initial = ""

    while True:
        word = get_next_word(rest)
        if not word:
            break

        initial = word[0].lower()
        if prev_initial and prev_initial == initial:
            return False

        prev_initial = initial
        rest = advance_to_next_word(rest)

    return True


def longest_sentence_no_same_initial_neighbors() -> str:
    current_sentence = read_sentece()
    best = ""

    while current_sentence:
        s = current_sentence.strip()

        if check(s):
            best = update_max(s, best)

        current_sentence = read_sentece()

    return best


def main() -> None:
    print(longest_sentence_no_same_initial_neighbors())


if __name__ == "__main__":
    run_main(main)
