from pathlib import Path
text = """# wypisuje 20 pierwszych zda?
import sys

from sentence_utils import is_end_of_sentence, read_char

sys.stdout.reconfigure(encoding=\"utf-8\")
sys.stdin.reconfigure(encoding=\"utf-8\")


def first_20_sentences():
    sentence_count = 0
    buffer = []

    while sentence_count < 20:
        c = read_char()
        if not c:
            break

        buffer.append(c)

        if is_end_of_sentence(c):
            sentence = "".join(buffer).strip()
            if sentence:
                print(sentence)
                sentence_count += 1
            buffer.clear()


if __name__ == \"__main__\":
    first_20_sentences()
"""
Path('app/first_20_senteces.py').write_text(text, encoding='utf-8')
