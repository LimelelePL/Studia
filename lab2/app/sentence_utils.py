# funkcje operujące na jednym zdaniu, np. zliczanie słów, liczenie spójników
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stdin.reconfigure(encoding="utf-8")


def is_end_of_sentence(c: str) -> bool:
    return c in ".!?"


def read_char() -> str:
    return sys.stdin.read(1)


def read_line() -> str:
    return sys.stdin.readline()


def read_sentece() -> str:
    result = ""
    prev_was_newline = False

    c = read_char()

    while c:
        result += c

        # zachowujemy strukture akapitu
        if is_end_of_sentence(c):
            c = read_char()
            while c == "\n":
                result += c
                c = read_char()
            return result

        elif c == "\n":
            if prev_was_newline:
                return result
            prev_was_newline = True
        else:
            prev_was_newline = False

        c = read_char()

    return result
