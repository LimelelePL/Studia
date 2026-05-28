import sys

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget


def run_gui():
    app = QApplication(sys.argv)
    main_window = main_widget()

    layout = QVBoxLayout()

    main_window.setLayout(layout)
    main_window.show()

    sys.exit(app.exec())


def main_widget() -> QWidget:
    window = QWidget()
    window.setWindowTitle("Log analyser")
    window.resize(960, 600)

    window.setStyleSheet("background-color: rgb(253, 245, 230);")

    return window
