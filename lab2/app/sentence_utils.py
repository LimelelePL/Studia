# funkcje operujące na jednym zdaniu, np. zliczanie słów, liczenie spójników
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")


def is_end_of_sentence(c: str) -> bool:
    return c in ".!?"


def read_char() -> str:
    return sys.stdin.read(1)


def read_line() -> str:
    return sys.stdin.readline()
