from sentence_utils import format_stream_utf8, read_sentece


def first_20_sentences() -> str:
    result = ""
    for _ in range(20):
        result += read_sentece()

    return result


if __name__ == "__main__":
    format_stream_utf8()
    print(first_20_sentences().strip())
