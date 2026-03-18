from sentence_utils import read_line, run_main


def count_paragraphs() -> int:
    paragraphs = 0
    is_prev_empty = True

    line = read_line()
    while line:
        if line.strip() == "":
            is_prev_empty = True
        else:
            if is_prev_empty:
                paragraphs += 1
            is_prev_empty = False

        line = read_line()
    return paragraphs


def main() -> None:
    print(f"Ilość akapitów: {count_paragraphs()}")


if __name__ == "__main__":
    run_main(main)
