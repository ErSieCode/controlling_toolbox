from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFileDialog, QComboBox, QTableView, QGroupBox,
                             QCheckBox, QLineEdit, QSpinBox)
from PyQt6.QtCore import pyqtSignal, Qt
import pandas as pd
from PyQt6.QtCore import QAbstractTableModel


class PandasModel(QAbstractTableModel):
    """Ein Model für die Anzeige von pandas DataFrames in QTableView"""

    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])
        return None


class ImportTab(QWidget):
    """Tab für den Import von Excel-Dateien"""

    # Signale für Kommunikation mit Controller
    file_selected = pyqtSignal(str)
    import_data = pyqtSignal(str, str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Initialisiert die UI-Komponenten"""
        layout = QVBoxLayout(self)

        # Dateiauswahl
        file_group = QGroupBox("Dateiauswahl")
        file_layout = QHBoxLayout(file_group)

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setPlaceholderText("Wählen Sie eine Excel-Datei aus...")

        self.browse_button = QPushButton("Durchsuchen...")
        self.browse_button.clicked.connect(self.browse_file)

        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(self.browse_button)

        # Tabellenblatt-Auswahl
        sheet_group = QGroupBox("Tabellenblatt")
        sheet_layout = QHBoxLayout(sheet_group)

        self.sheet_combo = QComboBox()
        self.sheet_combo.setEnabled(False)

        sheet_layout.addWidget(QLabel("Tabellenblatt:"))
        sheet_layout.addWidget(self.sheet_combo)

        # Import-Optionen
        options_group = QGroupBox("Import-Optionen")
        options_layout = QVBoxLayout(options_group)

        skip_layout = QHBoxLayout()
        skip_layout.addWidget(QLabel("Zeilen überspringen:"))
        self.skip_rows_spin = QSpinBox()
        self.skip_rows_spin.setRange(0, 100)
        skip_layout.addWidget(self.skip_rows_spin)
        skip_layout.addStretch()

        header_layout = QHBoxLayout()
        self.header_check = QCheckBox("Erste Zeile als Spaltennamen verwenden")
        self.header_check.setChecked(True)
        header_layout.addWidget(self.header_check)

        options_layout.addLayout(skip_layout)
        options_layout.addLayout(header_layout)

        # Import-Button
        self.import_button = QPushButton("Daten importieren")
        self.import_button.setEnabled(False)
        self.import_button.clicked.connect(self.import_file)

        # Datenvorschau
        preview_group = QGroupBox("Datenvorschau")
        preview_layout = QVBoxLayout(preview_group)

        self.preview_table = QTableView()
        preview_layout.addWidget(self.preview_table)

        # Alles zusammenfügen
        layout.addWidget(file_group)
        layout.addWidget(sheet_group)
        layout.addWidget(options_group)
        layout.addWidget(self.import_button)
        layout.addWidget(preview_group)

    def browse_file(self):
        """Öffnet einen Datei-Browser-Dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Excel-Datei öffnen",
            "",
            "Excel-Dateien (*.xlsx *.xls *.xlsm)"
        )

        if file_path:
            self.file_path_edit.setText(file_path)
            self.file_selected.emit(file_path)
            self.sheet_combo.setEnabled(True)
            self.import_button.setEnabled(True)

    def set_sheets(self, sheet_names):
        """Setzt die verfügbaren Tabellenblätter"""
        self.sheet_combo.clear()
        self.sheet_combo.addItems(sheet_names)

    def import_file(self):
        """Importiert die ausgewählte Datei"""
        file_path = self.file_path_edit.text()
        sheet_name = self.sheet_combo.currentText()

        # Import-Optionen sammeln
        options = {
            "skiprows": self.skip_rows_spin.value() if self.skip_rows_spin.value() > 0 else None,
            "header": 0 if self.header_check.isChecked() else None
        }

        # Signal emittieren
        self.import_data.emit(file_path, sheet_name, options)

    def update_preview(self, df):
        """Aktualisiert die Datenvorschau"""
        if df is not None:
            # Zeige nur die ersten 100 Zeilen in der Vorschau
            preview_df = df.head(100)
            model = PandasModel(preview_df)
            self.preview_table.setModel(model)

            # Spaltenbreiten anpassen
            self.preview_table.resizeColumnsToContents()