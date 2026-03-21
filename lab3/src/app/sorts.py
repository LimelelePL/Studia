from app.constants import RawLogIndex
from app.my_types import Entry


# sortuje malejaca czy rosnaca? oczywiscie cwel nie raczyl powiedziec jednoczenie napisal jake funkcja ma miec
# parametry wiec nie mozna przyjmowac parametru co do kolejnosci sortowanai
def sort_log(log: list[Entry], index: int) -> list[Entry]:
    max_index = len(RawLogIndex)
    if not (-max_index <= index < max_index):
        raise IndexError(f"Index out of range log range, last index is: {max_index} but {index} were given")

    log.sort(key=lambda x: (x[index] is None, x[index]))

    return log
