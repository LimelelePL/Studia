from sentence_utils import read_sentece, run_main


def first_20_sentences() -> str:
    result = ""
    for _ in range(20):
        result += read_sentece()

    return result


def main() -> None:
    print(first_20_sentences().strip())


if __name__ == "__main__":
    run_main(main)
