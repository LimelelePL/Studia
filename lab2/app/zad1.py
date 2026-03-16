import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

def echo(sentence):
    return "("+sentence+")"

def is_end_of_sentence(c: str) -> bool:
    return c in ".!?"


def skip_preamble() -> str:
    text = ""
    empty_counter = 0

    for i in range(10):
        c = sys.stdin.readline()
        text += c

        if not c:
            break

        if c == "\n":
            empty_counter += 1
        else:
            empty_counter = 0

        if empty_counter == 2:
            text = ""

    return text


def clean_inside_spaces(text: str) -> str:
    result = ""
    in_space = False

    for i in range (len(text)):
        ch = text[i]

        if ch.isspace():
            if not in_space:
                result += " "
                in_space = True
        else:
            result += ch
            in_space = False

    return result


def print_processed_sentence(sentence: str, process_sentence: callable) -> None:
    normalized_sentence = clean_inside_spaces(sentence.strip())
    if normalized_sentence:
        print(process_sentence(normalized_sentence))


def process_char(c : str, sentence: str, prev_was_newline : bool, process_sentence : callable) -> (str, bool):
    if c == "\n":
        if prev_was_newline:
            # pusty wiersz koniec akapitu i zdania
            print_processed_sentence(sentence, process_sentence)
            print()
            sentence = ""
        else:
            prev_was_newline = True
            sentence += c
    else:
        prev_was_newline = False
        sentence += c
        if is_end_of_sentence(c):
            print_processed_sentence(sentence, process_sentence)
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

    print_processed_sentence(sentence, process_sentence)



if __name__ == "__main__":
    try:
        main(echo)
    except BrokenPipeError:
        sys.exit(0)