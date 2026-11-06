from app.logs_parser.my_types import Entry


def sort_log(log: list[Entry], index: int) -> list[Entry]:
    # Klucz sortowania: (is_none, value):
    #   - is_none: True/False — Python sortuje False < True, więc wpisy z None trafiają na koniec
    #   - value: sama wartość pola — decyduje o kolejności wpisów, które nie są None
    max_index = len(Entry._fields)
    if not (-max_index <= index < max_index):
        raise IndexError(f"Index out of range log range, last index is: {max_index} but {index} were given")
    return sorted(log, key=lambda x: (x[index] is None, x[index]))
