import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()


def run_gui() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
