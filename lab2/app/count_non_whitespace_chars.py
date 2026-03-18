from sentence_utils import read_char, run_main


def count_non_whitespace_chars() -> int:
    counter = 0

    c = read_char()
    while c:
        if not c.isspace():
            counter += 1
        c = read_char()
    return counter


def main() -> None:
    print(f"Ilość znaków bez białych znaków: {count_non_whitespace_chars()}")


if __name__ == "__main__":
    run_main(main)
