import sys

from sentence_utils import read_sentece

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")


def first_20_sentences() -> str:
    result = ""
    for _ in range(5):
        result += read_sentece()

    return result


if __name__ == "__main__":
    print(first_20_sentences().strip())
