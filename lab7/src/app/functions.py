from functools import reduce


def acronym(entry: list[str]) -> str:
    return "".join(x[0] if x else " " for x in entry)


def median(entry: list[int]) -> float:
    sorted_entry = sorted(entry)
    mid1 = int((len(sorted_entry) - 1) / 2)
    mid2 = int(len(sorted_entry) / 2)
    return (sorted_entry[mid1] + sorted_entry[mid2]) / 2


def sqrt(x: float, epsilon: float) -> float:
    def step(y: float) -> float:
        return y if abs(y * y - x) < epsilon else step((y + x / y) / 2)

    return step(1.0 if x == 0 else x) if x != 0 else 0.0


def make_alpha_dict(entry: str) -> dict[str, list[str]]:
    result = {}
    [result.setdefault(word[0], []).append(word) for word in entry.split() if word[0].isalpha()]
    return result


def flatten(list):
    match list:
        case list() | tuple():
            return reduce(lambda acc, x: acc + flatten(x), list, [])
        case scalar:
            return [scalar]


def group_anagram(entry: list[str]) -> dict[str, list[str]]:
    result = {}
    [result.setdefault("".join(sorted(word)), []).append(word) for word in entry]
    return result


# zad 2 - wersja z builtins
def forall(pred, iterable) -> bool:
    return all(map(pred, iterable))


def exists(pred, iterable) -> bool:
    return any(map(pred, iterable))


def atleast(n: int, pred, iterable) -> bool:
    return sum(map(pred, iterable)) >= n


def atmost(n: int, pred, iterable) -> bool:
    return sum(map(pred, iterable)) <= n


# zad 2 - wersja z reduce
def forall_reduce(pred, iterable) -> bool:
    return reduce(lambda acc, x: acc and bool(pred(x)), iterable, True)


def exists_reduce(pred, iterable) -> bool:
    return reduce(lambda acc, x: acc or bool(pred(x)), iterable, False)


def atleast_reduce(n: int, pred, iterable) -> bool:
    return reduce(lambda acc, x: acc + bool(pred(x)), iterable, 0) >= n


def atmost_reduce(n: int, pred, iterable) -> bool:
    return reduce(lambda acc, x: acc + bool(pred(x)), iterable, 0) <= n
