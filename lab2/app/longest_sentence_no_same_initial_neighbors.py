# Wypisuje najdłuższe zdanie, w którym żadne dwa
# sąsiadujące słowa nie zaczynają się na tę samą literę.
from sentence_utils import read_sentece, skip_spaces, update_max


def check(sentence: str) -> bool:
    sentence = sentence.strip()
    first_idx = 0

    while first_idx < len(sentence):
        first = ""
        second = ""

        # pomijamy spacje przed pierwszym słowem
        first_idx = skip_spaces(sentence, first_idx)

        if first_idx >= len(sentence):
            break

        # szukamy pierwszego słowa
        while first_idx < len(sentence):
            if sentence[first_idx].isspace():
                break
            first += sentence[first_idx]
            first_idx += 1

        # pomijamy spacje przed drugim słowem
        second_idx = skip_spaces(sentence, first_idx)

        if second_idx >= len(sentence):
            break

        # szukamy kolejnego słowa
        while second_idx < len(sentence):
            if sentence[second_idx].isspace():
                break
            second += sentence[second_idx]
            second_idx += 1

        if first and second:
            if first[0].lower() == second[0].lower():
                return False

        first_idx = second_idx

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


if __name__ == "__main__":
    print(longest_sentence_no_same_initial_neighbors())
