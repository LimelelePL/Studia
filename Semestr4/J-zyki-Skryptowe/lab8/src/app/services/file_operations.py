from pathlib import Path

from app.logs_parser.constants import EMPTY_ENTRY
from app.logs_parser.converters import _extract_raw_entry_fields, _normalize_raw_entry
from app.logs_parser.my_types import Entry


def parse_file(path: Path) -> list[Entry]:
    log: list[Entry] = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if raw_log_line := line.strip():
                try:
                    log.append(_normalize_raw_entry(_extract_raw_entry_fields(raw_log_line)))
                except (IndexError, ValueError):
                    log.append(EMPTY_ENTRY)
    return log
