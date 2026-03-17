# Wypisuje pierwsze zdanie, które ma więcej niż jedno zdanie podrzędne,
# czyli w praktyce ma więcej niż jeden przecinek
from sentence_utils import read_sentece


def first_sentence_with_many_subordinates() -> str:
    sentece = ""
    found = False

    while not found:
        sentece = read_sentece().strip()

        if not sentece:
            break

        comma_counter = 0

        for w in sentece:
            if w == ",":
                comma_counter += 1
            if comma_counter == 2:
                found = True

    return sentece if found else ""


if __name__ == "__main__":
    print(first_sentence_with_many_subordinates())
