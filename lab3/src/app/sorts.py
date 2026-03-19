from app.types import Entry


# sortuje malejaca czy rosnaca? oczywiscie cwel nie raczyl powiedziec jednoczenie napisal jake funkcja ma miec
# parametry wiec nie mozna przyjmowac parametru co do kolejnosci sortowanai
def sort_log(log: list[Entry], index: int) -> list[Entry]:

    size = len(log[0])

    if not (-size <= index < size):
        raise IndexError("Niepoprawny index")

    log.sort(key=lambda x: (x[index] is None, x[index]))

    return log
