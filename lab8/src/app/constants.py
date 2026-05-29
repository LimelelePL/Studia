from typing import Final

DETAIL_LINE_EDIT_NAMES: Final[tuple[str, ...]] = (
    "remoteHostLineEdit",
    "dateLineEdit",
    "timeLineEdit",
    "timezoneLineEdit",
    "statusCodeLineEdit",
    "methodLineEdit",
    "sizeLineEdit",
)

RESOURCE_WIDGET_NAME: Final[str] = "resourcePlainTextEdit"
RESOURCE_DETAIL_INDEX: Final[int] = 6
DETAIL_LINE_EDIT_VALUE_INDICES: Final[tuple[int, ...]] = (0, 1, 2, 3, 4, 5, 7)
