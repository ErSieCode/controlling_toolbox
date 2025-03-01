from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QTableView, QGroupBox,
                             QFormLayout, QLineEdit)
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


class AnalysisTab(QWidget):
    """Tab für die Datenanalyse"""

    # Signal für Kommunikation mit Controller
    run_analysis = pyqtSignal(str, str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_sources = []
        self.init_ui()

    def init_ui(self):
        """Initialisiert die UI-Komponenten"""
        layout = QVBoxLayout(self)

        # Datenauswahl
        data_group = QGroupBox("Datenauswahl")
        data_layout = QFormLayout(data_group)

        self.data_combo = QComboBox()
        data_layout.addRow("Datensatz:", self.data_combo)

        # Analysetyp-Auswahl
        self.analysis_combo = QComboBox()
        self.analysis_combo.addItems(["KPI-Berechnung", "Abweichungsanalyse"])
        self.analysis_combo.currentIndexChanged.connect(self.on_analysis_type_changed)
        data_layout.addRow("Analysetyp:", self.analysis_combo)

        # KPI-Parameter
        self.kpi_group = QGroupBox("KPI-Parameter")
        kpi_layout = QFormLayout(self.kpi_group)

        self.revenue_col_edit = QLineEdit("Umsatz")
        self.cost_col_edit = QLineEdit("Kosten")
        self.time_col_edit = QLineEdit("Datum")

        kpi_layout.addRow("Umsatzspalte:", self.revenue_col_edit)
        kpi_layout.addRow("Kostenspalte:", self.cost_col_edit)
        kpi_layout.addRow("Zeitspalte:", self.time_col_edit)

        # Abweichungsanalyse-Parameter
        self.variance_group = QGroupBox("Abweichungsanalyse-Parameter")
        variance_layout = QFormLayout(self.variance_group)

        self.plan_data_combo = QComboBox()
        self.key_column_edit = QLineEdit("Monat")
        self.value_columns_edit = QLineEdit("Umsatz,Kosten")

        variance_layout.addRow("Plan-Datensatz:", self.plan_data_combo)
        variance_layout.addRow("Schlüsselspalte:", self.key_column_edit)
        variance_layout.addRow("Wertspalten (kommagetrennt):", self.value_columns_edit)

        # Analysebutton
        self.run_button = QPushButton("Analyse durchführen")
        self.run_button.clicked.connect(self.run_selected_analysis)

        # Analyseergebnis
        result_group = QGroupBox("Analyseergebnis")
        result_layout = QVBoxLayout(result_group)

        self.result_table = QTableView()
        result_layout.addWidget(self.result_table)

        # Alles zusammenfügen
        layout.addWidget(data_group)
        layout.addWidget(self.kpi_group)
        layout.addWidget(self.variance_group)
        layout.addWidget(self.run_button)
        layout.addWidget(result_group)

        # Standardeinstellung: KPI-Berechnung anzeigen, Abweichungsanalyse ausblenden
        self.variance_group.setVisible(False)

    def on_analysis_type_changed(self, index):
        """Wird aufgerufen, wenn der Analysetyp geändert wird"""
        if index == 0:  # KPI-Berechnung
            self.kpi_group.setVisible(True)
            self.variance_group.setVisible(False)
        elif index == 1:  # Abweichungsanalyse
            self.kpi_group.setVisible(False)
            self.variance_group.setVisible(True)

    def set_data_sources(self, data_keys):
        """Setzt die verfügbaren Datensätze"""
        self.data_sources = data_keys

        # Aktuellen Text speichern
        current_data = self.data_combo.currentText()
        current_plan = self.plan_data_combo.currentText()

        # Comboboxen leeren und neu füllen
        self.data_combo.clear()
        self.plan_data_combo.clear()

        self.data_combo.addItems(data_keys)
        self.plan_data_combo.addItems(data_keys)

        # Wenn möglich, vorherige Auswahl wiederherstellen
        if current_data in data_keys:
            self.data_combo.setCurrentText(current_data)

        if current_plan in data_keys:
            self.plan_data_combo.setCurrentText(current_plan)

    def run_selected_analysis(self):
        """Führt die ausgewählte Analyse durch"""
        data_key = self.data_combo.currentText()

        if not data_key:
            return

        analysis_index = self.analysis_combo.currentIndex()

        if analysis_index == 0:  # KPI-Berechnung
            analysis_type = "kpi"
            parameters = {
                "revenue_col": self.revenue_col_edit.text(),
                "cost_col": self.cost_col_edit.text(),
                "time_col": self.time_col_edit.text() if self.time_col_edit.text() else None
            }
        elif analysis_index == 1:  # Abweichungsanalyse
            analysis_type = "variance"

            # Werte aus den Feldern abrufen
            plan_data_key = self.plan_data_combo.currentText()
            key_column = self.key_column_edit.text()
            value_columns_text = self.value_columns_edit.text()

            # Wertspalten als Liste
            value_columns = [col.strip() for col in value_columns_text.split(",") if col.strip()]

            parameters = {
                "plan_data_key": plan_data_key,
                "key_column": key_column,
                "value_columns": value_columns
            }
        else:
            return

        # Signal emittieren
        self.run_analysis.emit(data_key, analysis_type, parameters)

    def show_result(self, df):
        """Zeigt das Analyseergebnis an"""
        if df is not None:
            model = PandasModel(df)
            self.result_table.setModel(model)

            # Spaltenbreiten anpassen
            self.result_table.resizeColumnsToContents()