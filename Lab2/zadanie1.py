import sys


def echo(sentence : str) -> str:
    return "("+sentence+")"

def skip_preamble() -> bool:
    empty_row = 0

    for i in range(10):
        c = sys.stdin.readline()

        if c == "":
            break #koniec pliku

        if c == "\n":
            empty_row += 1
        else:
            empty_row = 0

        if empty_row == 2:
            return True

    return False

def main(process_sentence: callable) -> None:
    skip_preamble()

    sentence = ""
    ending = "-----"

    c = sys.stdin.read(1)

    while c:
        sentence += c

        if sentence.endswith(ending):
            break

        if c in ".":
            print(process_sentence(sentence.strip()))
            sentence = ""

        c = sys.stdin.read(1)


if __name__ == "__main__":
    main(echo)