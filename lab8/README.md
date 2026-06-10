# PySide6 / PyQt Cheat Sheet

Krotka sciaga z podstawowych widgetow i najczestszych sygnalow.

## Najczestsze widgety

- `QMainWindow` - glowne okno aplikacji
- `QWidget` - bazowy kontener
- `QLabel` - wyswietlanie tekstu
- `QPushButton` - przycisk
- `QLineEdit` - jednolinijkowe pole tekstowe
- `QPlainTextEdit` - dluzszy tekst, dobre do logow i URI
- `QListWidget` - prosta lista elementow
- `QComboBox` - lista rozwijana
- `QCheckBox` - checkbox
- `QDateEdit` - wybor daty
- `QDateTimeEdit` - wybor daty i czasu
- `QSpinBox` - liczby calkowite

## Widgety czesto dawane do modyfikacji

- `QRadioButton` - wybor jednej opcji, np. `GET / HEAD / ALL`
- `QTableWidget` - tabela logow zamiast zwyklej listy
- `QTreeWidget` - lista z kolumnami albo drzewkiem
- `QSlider` - zakres lub limit, np. max liczba wynikow
- `QTabWidget` - zakladki, np. `Lista / Statystyki`
- `QGroupBox` - grupowanie filtrow
- `QTextEdit` - wieksze pole tekstowe z formatowaniem
- `QFileDialog` - wybor pliku z logami

## Najczestsze sygnaly

- `QPushButton`
  - `clicked`
  - `pressed`

- `QLineEdit`
  - `textChanged`
  - `editingFinished`
  - `returnPressed`

- `QPlainTextEdit`
  - `textChanged`

- `QListWidget`
  - `currentRowChanged`
  - `itemClicked`
  - `itemSelectionChanged`

- `QComboBox`
  - `currentTextChanged`
  - `currentIndexChanged`
  - `activated`

- `QCheckBox`
  - `toggled`
  - `stateChanged`
  - `checkStateChanged`

- `QRadioButton`
  - `toggled`
  - `clicked`

- `QDateEdit` / `QDateTimeEdit`
  - `dateChanged`
  - `dateTimeChanged`
  - `timeChanged`

- `QSpinBox`
  - `valueChanged`

- `QSlider`
  - `valueChanged`
  - `sliderMoved`

## Typowe podpinanie sygnalow

```python
self.ui.browseButton.clicked.connect(self.browse_file)
self.ui.comboFilterExtension.currentTextChanged.connect(self.apply_filters)
self.ui.only_extensions_checkbox.toggled.connect(self.apply_filters)
self.ui.logListWidget.currentRowChanged.connect(self.show_log_details)
self.ui.DateFrom.dateTimeChanged.connect(self.apply_filters)
```

## Typowe akcje na widgetach

- `QLabel`
  - `setText(...)`

- `QLineEdit`
  - `setText(...)`
  - `text()`
  - `clear()`

- `QPlainTextEdit`
  - `setPlainText(...)`
  - `toPlainText()`
  - `clear()`

- `QListWidget`
  - `addItems(...)`
  - `clear()`
  - `setCurrentRow(...)`
  - `currentRow()`

- `QComboBox`
  - `addItems(...)`
  - `currentText()`
  - `setCurrentIndex(...)`

- `QCheckBox`
  - `isChecked()`
  - `setChecked(...)`

- `QDateTimeEdit`
  - `dateTime()`
  - `setDateTime(...)`

## Run

Instalacja zaleznosci:

```bash
uv sync
```

Uruchomienie aplikacji:

```bash
uv run lab8
```

Uruchomienie Qt Designera:

```bash
uv run pyside6-designer
```

Przetlumaczenie pliku `.ui` na `.py`:

```bash
uv run pyside6-uic src/app/gui/main_window.ui -o src/app/gui/ui_main_window.py
```
