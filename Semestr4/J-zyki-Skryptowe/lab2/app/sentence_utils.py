# funkcje operujące na jednym zdaniu, np. zliczanie słów, liczenie spójników
import sys


def is_end_of_sentence(c: str) -> bool:
    return c in ".!?"


def read_char() -> str:
    return sys.stdin.read(1)


def read_line() -> str:
    return sys.stdin.readline()


def update_max(current: str, best: str) -> str:
    if len(current) > len(best):
        return current
    return best


def skip_spaces(sentence: str, idx: int) -> int:
    while idx < len(sentence) and sentence[idx].isspace():
        idx += 1
    return idx


def skip_word(s: str) -> str:
    i = 0
    while i < len(s):
        if s[i].isalpha():
            i += 1
        elif s[i] in "-'" and i + 1 < len(s) and s[i + 1].isalpha():
            i += 1  # myślnik/apostrof wewnątrz słowa
        else:
            break
    return s[i:]


def skip_non_alpha(s: str) -> str:
    i = 0
    while i < len(s) and not s[i].isalpha():
        i += 1
    return s[i:]


def advance_to_next_word(s: str) -> str:
    return skip_non_alpha(skip_word(s))


def get_next_word(s: str) -> str:
    s = skip_non_alpha(s)
    if not s:
        return ""

    rest = skip_word(s)
    return s[: len(s) - len(rest)]


def read_sentece() -> str:
    result = ""
    prev_was_newline = False

    c = read_char()
    while c:
        result += c

        if is_end_of_sentence(c):
            return result

        if c == "\n":
            if prev_was_newline:
                return result
            prev_was_newline = True
        else:
            prev_was_newline = False

        c = read_char()

    return result


def format_stream_utf8() -> None:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")


def run_main(fn) -> None:
    format_stream_utf8()
    try:
        fn()
    except BrokenPipeError:
        pass
    except KeyboardInterrupt:
        pass
    except ValueError as e:
        print(f"Błąd: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        try:
            sys.stdout.flush()
        except BrokenPipeError:
            pass
        try:
            sys.stderr.flush()
        except BrokenPipeError:
            pass
