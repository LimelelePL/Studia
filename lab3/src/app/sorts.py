from app.types import HttpEntry


# sortuje malejaca czy rosnaca? oczywiscie cwel nie raczyl powiedziec jednoczenie napisal jake funkcja ma miec
# parametry wiec nie mozna przyjmowac parametru co do kolejnosci sortowanai
def sort_log(logs: list[HttpEntry], index: int) -> list[HttpEntry]:

    size = len(logs[0])

    if not (-size <= index < size):
        raise IndexError("Niepoprawny index")

    logs.sort(key=lambda x: (x[index] is None, x[index]))

    return logs
