from sentence_utils import advance_to_next_word, read_sentece, run_main, skip_non_alpha

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")


def has_proper_name(sentence: str) -> bool:
    sentence = advance_to_next_word(skip_non_alpha(sentence))

    while sentence:
        if sentence[0].isupper():
            return True
        sentence = advance_to_next_word(sentence)

    return False


def percent_sentences_with_proper_name() -> float:
    total = 0
    with_proper_name = 0

    sentence = read_sentece()
    while sentence:
        if sentence.strip():
            total += 1
            if has_proper_name(sentence):
                with_proper_name += 1
        sentence = read_sentece()

    if total == 0:
        raise ValueError("Brak zdań w tekście")

    return (with_proper_name / total) * 100


def main() -> None:
    result = percent_sentences_with_proper_name()
    print(f"Procent zdań z nazwą własną: {result:.2f}%")


if __name__ == "__main__":
    run_main(main)
