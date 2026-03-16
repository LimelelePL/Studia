#wypisuje 20 pierwszych zdań

import sys
import io

from lab2.app.sentence_utils import read_line, read_char

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

def first_20_sentences():

if __name__ == "__main__":
    first_20_sentences()
