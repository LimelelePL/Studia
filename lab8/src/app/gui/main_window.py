import datetime
import sys
from pathlib import Path
from typing import cast

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLineEdit,
    QMainWindow,
)

from app.constants import DETAIL_WIDGET_NAMES
from app.gui.ui_main_window import Ui_MainWindow
from app.logs_parser.my_types import Entry
from app.services.log_service import (
    build_detail_values,
    build_entry_summaries,
    load_entries,
    logs_in_time_range,
    min_max_timestamp,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui: Ui_MainWindow = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entries: list[Entry] = []
        self.filtered_entries: list[Entry] = []
        self.current_file_path: Path | None = None
        self.current_row: int = -1

        self.ui.browseButton.clicked.connect(self.browse_file)
        self.ui.DateFrom.dateTimeChanged.connect(self.filter_logs_by_date)
        self.ui.DateTo.dateTimeChanged.connect(self.filter_logs_by_date)
        self.ui.logListWidget.currentRowChanged.connect(self.show_log_details)
        self.ui.previousButton.clicked.connect(self.prev_button)
        self.ui.nextButton.clicked.connect(self.next_button)

        self.details_labels: list[QLineEdit] = [cast(QLineEdit, getattr(self.ui, name)) for name in DETAIL_WIDGET_NAMES]

    def browse_file(self):
        start_dir = str(self.current_file_path.parent) if self.current_file_path else str(Path.cwd())

        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption="wybierz plik z logami",
            filter="Log file (*.log)",
            dir=start_dir,
        )
        if not file_path:
            return

        self.ui.selectedFileLineEdit.setText(file_path)
        self.load_logs_list(Path(file_path))

    def load_logs_list(self, path: Path):
        self.entries = load_entries(path)
        self.filtered_entries = self.entries.copy()
        self.current_file_path = path
        self.set_default_date_range()
        self.reload_log_list()

    def set_default_date_range(self):
        res = min_max_timestamp(self.entries)
        if not res:
            now = QDateTime.currentDateTime()
            self.ui.DateFrom.setDateTime(now)
            self.ui.DateTo.setDateTime(now)
            return

        first_ts, last_ts = res

        self.ui.DateFrom.setDateTime(QDateTime.fromMSecsSinceEpoch(round(first_ts.timestamp() * 1000)))
        self.ui.DateTo.setDateTime(QDateTime.fromMSecsSinceEpoch(round(last_ts.timestamp() * 1000)))

    def filter_logs_by_date(self, _date_time):
        # bo mypy krzyczy
        from_dt = cast(datetime.datetime, self.ui.DateFrom.dateTime().toPython())
        to_dt = cast(datetime.datetime, self.ui.DateTo.dateTime().toPython())

        self.filtered_entries = logs_in_time_range(self.entries, from_dt, to_dt)
        self.reload_log_list()

    def reload_log_list(self):
        self.ui.logListWidget.clear()
        self.ui.logListWidget.addItems(build_entry_summaries(self.filtered_entries))

        if len(self.filtered_entries) == 0:
            self.current_row = -1
            for field in self.details_labels:
                field.clear()
            self.update_navigation_buttons()
            return

        self.current_row = 0
        self.ui.logListWidget.setCurrentRow(self.current_row)
        self.update_navigation_buttons()

    def show_log_details(self, row: int):
        self.current_row = row

        self.update_navigation_buttons()

        for field in self.details_labels:
            field.clear()

        if self.current_row < 0 or self.current_row >= len(self.filtered_entries):
            return

        entry = self.filtered_entries[self.current_row]
        for widget, value in zip(self.details_labels, build_detail_values(entry), strict=True):
            widget.setText(value)

    def next_button(self):
        if self.current_row >= len(self.filtered_entries) - 1 or self.current_row == -1:
            return

        self.current_row += 1
        self.ui.logListWidget.setCurrentRow(self.current_row)

    def prev_button(self):
        if self.current_row <= 0:
            return

        self.current_row -= 1
        self.ui.logListWidget.setCurrentRow(self.current_row)

    def update_navigation_buttons(self):
        self.ui.previousButton.setEnabled(self.current_row > 0)
        self.ui.nextButton.setEnabled(0 <= self.current_row < len(self.filtered_entries) - 1)


def run_gui() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
