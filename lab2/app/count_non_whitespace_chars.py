# zlicza wszystkie znaki oprócz białych znaków

from lab2.app.sentence_utils import read_char


def count_non_whitespace_chars():
    counter = 0

    c = read_char()
    while c:
        if not c.isspace():
            counter += 1
        c = read_char()

    print("ilosc znakow bez bialych znakow ", counter)


if __name__ == "__main__":
    count_non_whitespace_chars()
