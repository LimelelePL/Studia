#Zlicza akapity oddzielone pustą linią.
#Na wejściu tekst, na wyjściu jedna liczba.
from sentence_utils import *

def count_paragraphs():
    paragraphs = 0
    is_prev_empty = False

    line = sys.stdin.readline()
    while line:
        if line.strip() == "":
            is_prev_empty = True
        else:
            if is_prev_empty:
                paragraphs += 1
            is_prev_empty = False

        line = sys.stdin.readline()

        print_using_stream("ilosc akapitów: ",str(paragraphs))

if __name__ == "__main__":
    count_paragraphs()
