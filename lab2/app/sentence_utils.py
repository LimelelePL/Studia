# funkcje operujące na jednym zdaniu, np. zliczanie słów, liczenie spójników
import sys

def print_using_stream(message : str, sentence : str) -> None:
    sys.stdout.write("\n")
    sys.stdout.write(message + sentence + "\n")