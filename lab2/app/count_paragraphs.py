from sentence_utils import read_line


def count_paragraphs():
    paragraphs = 0
    is_prev_empty = False

    line = read_line()
    while line:
        if line.strip() == "":
            is_prev_empty = True
        else:
            if is_prev_empty:
                paragraphs += 1
            is_prev_empty = False

        line = read_line()


if __name__ == "__main__":
    print(f"Ilość paragrafów {count_paragraphs()}")
