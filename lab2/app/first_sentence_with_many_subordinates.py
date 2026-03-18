from sentence_utils import read_sentece, run_main


def first_sentence_with_many_subordinates() -> str:
    sentence = read_sentece().strip()
    while sentence:
        comma_count = 0
        for ch in sentence:
            if ch == ",":
                comma_count += 1
                if comma_count == 2:
                    return sentence
        sentence = read_sentece().strip()
    return ""


def main() -> None:
    print(first_sentence_with_many_subordinates())


if __name__ == "__main__":
    run_main(main)
