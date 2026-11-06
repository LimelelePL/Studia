from sentence_utils import format_stream_utf8, read_sentece


def count_chars(sentence: str) -> int:
    counter = 0
    for c in sentence:
        counter += 1
    return counter


def count_avg_chars() -> float:
    total_sentences = 0
    total_chars = 0

    sentence = read_sentece()
    while sentence:
        total_sentences += 1
        total_chars += count_chars(sentence)
        sentence = read_sentece()

    if total_sentences == 0:
        raise ValueError("Brak zdań w tekście")
    return total_chars / total_sentences


def main() -> None:
    print(f"Średnia ilość znaków w zdaniu: {count_avg_chars()}")


if __name__ == "__main__":
    format_stream_utf8()
    main()
