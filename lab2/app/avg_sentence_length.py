from sentence_utils import read_sentece


def calc_avg_sentence_length() -> int:
    sentence = read_sentece()

    sum_of_length = 0
    no_of_senteces = 0

    while sentence:
        sum_of_length += len(sentence.strip())
        no_of_senteces += 1
        sentence = read_sentece()

    if no_of_senteces == 0:
        raise Exception("No sentences found")

    return sum_of_length / no_of_senteces


if __name__ == "__main__":
    test2 = (len("dwa znaki.".strip()) + len("trzy znaki".strip())) / 2
    print(test2)
    print(calc_avg_sentence_length())
