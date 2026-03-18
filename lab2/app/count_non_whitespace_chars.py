# zlicza wszystkie znaki oprócz białych znaków

from sentence_utils import read_char


def count_non_whitespace_chars():
    counter = 0

    c = read_char()
    while c:
        if not c.isspace():
            counter += 1
        c = read_char()
    return counter


if __name__ == "__main__":
    print(f"Iosc znakow bez bialych znakow {count_non_whitespace_chars()}")
