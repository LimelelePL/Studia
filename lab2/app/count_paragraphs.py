#Zlicza akapity oddzielone pustą linią.
#Na wejściu tekst, na wyjściu jedna liczba.
from sentence_utils import *

def count_paragraphs():
    paragraphs = 0
    is_prev_empty = False

    line = read_line()
    while line:
        if line.strip() == "":
            is_prev_empty = True
        else:
            if is_prev_empty:
                paragraphs += 1
            is_prev_empty = False

        line = read_line()

    print("ilosc paragrafow ", paragraphs)

if __name__ == "__main__":
    count_paragraphs()
