from enum import IntEnum
from typing import Final, cast

from app.my_types import Entry

EMPTY_FIELD: Final = "-"


# this enum is iterable, this class must have exaclty the same number of entres as EntryIndex
# in order to keep sort_log working
class RawLogIndex(IntEnum):
    TS = 0
    UID = 1
    ORIG_H = 2
    ORIG_P = 3
    RESP_H = 4
    RESP_P = 5
    METHOD = 7
    HOST = 8
    URI = 9
    STATUS_CODE = 14


class EntryIndex:
    TS: Final = 0
    UID: Final = 1
    ORIG_H: Final = 2
    ORIG_P: Final = 3
    RESP_H: Final = 4
    RESP_P: Final = 5
    METHOD: Final = 6
    HOST: Final = 7
    URI: Final = 8
    STATUS_CODE: Final = 9


ENTRY_INDEXES_WITH_IP: Final = (EntryIndex.ORIG_H, EntryIndex.RESP_H, EntryIndex.HOST)

RAW_LOG_FIELD_INDEXES: Final = tuple(RawLogIndex)

EMPTY_ENTRY = cast(Entry, (None,) * len(RawLogIndex))
