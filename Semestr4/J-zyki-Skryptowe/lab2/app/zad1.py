from sentence_utils import read_line, read_sentece, run_main


def skip_preamble() -> str:
    text = ""
    prev_empty = False

    for _ in range(10):
        line = read_line()

        if not line:
            break

        if line.strip() == "":
            if prev_empty:
                text = ""
            else:
                prev_empty = True
                text += line
        else:
            prev_empty = False
            text += line

    return text


def clean_inside_spaces(text: str) -> str:
    result = ""
    pending_space = False
    at_line_start = True

    for ch in text:
        if ch == "\n":
            pending_space = False
            result += "\n"
            at_line_start = True
        elif ch.isspace():
            if not at_line_start:
                pending_space = True
        else:
            if pending_space:
                result += " "
                pending_space = False
            at_line_start = False
            result += ch

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
        sentence = read_sentece()
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
    run_main(main)
