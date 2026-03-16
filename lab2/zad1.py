import sys

def echo(sentence):
    return "("+sentence+")"

def is_end_of_sentence(c):
    return c in ".!?"


def skip_preamble() -> str:
    text = ""
    empty_counter = 0
    newline_counter = 0

    while newline_counter < 10:
        c = sys.stdin.read(1)
        text += c

        if not c:
            break

        if c == "\n":
            empty_counter += 1
            newline_counter += 1
        else:
            empty_counter = 0

        if empty_counter == 3:
            text = ""

    return text


def process_char(c : str, sentence: str, prev_was_newline : bool, process_sentence : callable) -> (str, bool):
    if c == "\n":
        if prev_was_newline:
            # pusty wiersz koniec akapitu i zdania
            if sentence.strip():
                print(process_sentence(sentence.strip()))
            print()
            sentence = ""
        else:
            prev_was_newline = True
            sentence += c
    else:
        prev_was_newline = False
        sentence += c
        if is_end_of_sentence(c):
            print(process_sentence(sentence.strip()))
            sentence = ""

    return sentence, prev_was_newline

def check_ending(sentence : str) -> bool:
    return sentence.endswith("-----")


def process_preamble(process_sentence : callable) -> None:
    preamble = skip_preamble()

    if not preamble.strip():
        return

    sentence = ""
    prev_was_newline = False
    for p in preamble:
        sentence, prev_was_newline = process_char(p, sentence, prev_was_newline, process_sentence)
        if check_ending(sentence):
            break


def main(process_sentence):
    process_preamble(echo)

    sentence = ""
    prev_was_newline = False
    c = sys.stdin.read(1)

    while c:
        sentence, prev_was_newline = process_char(c, sentence, prev_was_newline, process_sentence)
        if check_ending(sentence):
            sentence = sentence[:-5]
            break
        c = sys.stdin.read(1)

    if sentence.strip():
        print(process_sentence(sentence.strip()))


if __name__ == "__main__":
    main(echo)