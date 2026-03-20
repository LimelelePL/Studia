import pytest

from app.constants import EntryIndex
from app.sorts import sort_log
from app.types import Entry


def test_sort_by_status_code(log: list[Entry]) -> None:
    sorted_log = sort_log(list(log), EntryIndex.STATUS_CODE)
    non_none = [e[EntryIndex.STATUS_CODE] for e in sorted_log if e[EntryIndex.STATUS_CODE] is not None]
    assert non_none == sorted(non_none)


def test_sort_nones_last(log: list[Entry]) -> None:
    sorted_log = sort_log(list(log), EntryIndex.STATUS_CODE)
    none_seen = False
    for entry in sorted_log:
        if entry[EntryIndex.STATUS_CODE] is None:
            none_seen = True
        else:
            assert not none_seen, "None values should be at the end"


def test_sort_invalid_index_raises(log: list[Entry]) -> None:
    with pytest.raises(IndexError):
        sort_log(list(log), 999)
