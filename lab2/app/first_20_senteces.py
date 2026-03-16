#wypisuje 20 pierwszych zdań

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

def first_20_sentences():
    senteces = 0
    while senteces < 20:
        line = sys.stdin.readline()

        if not line:
            break

        # zakladam ze sama pusta linia to nie zdanie
        if line != "\n":
            senteces += 1

        sys.stdout.write(line)

if __name__ == "__main__":
    first_20_sentences()
