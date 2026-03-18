# najdłuższe zdanie według liczby znaków

from sentence_utils import read_sentece, run_main, update_max


def longest_sentence() -> str:
    current_sentence = read_sentece()
    if not current_sentence:
        return ""

    current_sentence = current_sentence.strip()
    max_sentence = current_sentence

    while current_sentence:
        max_sentence = update_max(current_sentence, max_sentence)
        current_sentence = read_sentece()

        if current_sentence:
            current_sentence = current_sentence.strip()

    return max_sentence


def main() -> None:
    print(longest_sentence())


if __name__ == "__main__":
    run_main(main)
