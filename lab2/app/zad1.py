import io
import sys

from sentence_utils import get_sentece

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")


def skip_preamble() -> str:
    text = ""
    empty_counter = 0
    was_prev_empty = False

    for _ in range(10):
        sentence = get_sentece()

        if not sentence:
            break

        if sentence.strip() == "":
            was_prev_empty = True
            empty_counter += 1
            if empty_counter == 2:
                text = ""
        else:
            if was_prev_empty:
                text += "\n"
            was_prev_empty = False
            empty_counter = 0

        text += sentence

    return text


def clean_inside_spaces(text: str) -> str:
    result = ""
    was_space = False

    for ch in text:
        # zachowujemy akapity
        if ch == "\n":
            result += "\n"
            was_space = False
        elif ch.isspace():
            if not was_space:
                result += " "
                was_space = True
        else:
            result += ch
            was_space = False

    return result


def print_processed_sentence(sentence: str) -> None:
    normalized_sentence = clean_inside_spaces(sentence)
    if normalized_sentence.strip() == "":
        return

    print(normalized_sentence)


def has_ending_marker(text: str) -> bool:
    return text.find("-----") != -1


def remove_ending_marker(text: str) -> str:
    marker_idx = text.find("-----")
    if marker_idx == -1:
        return text
    return text[:marker_idx]


def process_preamble() -> None:
    preamble = skip_preamble()
    if not preamble.strip():
        return

    preamble = remove_ending_marker(preamble)
    print_processed_sentence(preamble)


def main() -> None:
    process_preamble()

    should_stop = False
    while not should_stop:
        sentence = get_sentece()
        if not sentence:
            break

        if has_ending_marker(sentence):
            sentence = remove_ending_marker(sentence)
            should_stop = True

        if sentence.strip() == "":
            print()
        else:
            print_processed_sentence(sentence)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)
