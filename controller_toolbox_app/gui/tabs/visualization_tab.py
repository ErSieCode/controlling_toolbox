from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QGroupBox, QFormLayout, QLineEdit)
from PyQt6.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class VisualizationTab(QWidget):
    """Tab für die Datenvisualisierung"""

    # Signal für Kommunikation mit Controller
    create_chart = pyqtSignal(str, str, dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_sources = []
        self.init_ui()

    def init_ui(self):
        """Initialisiert die UI-Komponenten"""
        layout = QVBoxLayout(self)

        # Oberer Bereich: Einstellungen
        settings_layout = QHBoxLayout()

        # Datenauswahl
        data_group = QGroupBox("Datenauswahl")
        data_layout = QFormLayout(data_group)

        self.data_combo = QComboBox()
        data_layout.addRow("Datensatz:", self.data_combo)

        # Diagrammtyp-Auswahl
        self.chart_combo = QComboBox()
        self.chart_combo.addItems(["Zeitreihendiagramm", "Abweichungsdiagramm"])
        self.chart_combo.currentIndexChanged.connect(self.on_chart_type_changed)
        data_layout.addRow("Diagrammtyp:", self.chart_combo)

        settings_layout.addWidget(data_group)

        # Zeitreihendiagramm-Parameter
        self.timeseries_group = QGroupBox("Zeitreihendiagramm-Parameter")
        timeseries_layout = QFormLayout(self.timeseries_group)

        self.x_col_edit = QLineEdit("Datum")
        self.y_col_edit = QLineEdit("Umsatz")
        self.title_edit = QLineEdit("Zeitreihenanalyse")

        timeseries_layout.addRow("X-Achse (Zeit):", self.x_col_edit)
        timeseries_layout.addRow("Y-Achse (Wert):", self.y_col_edit)
        timeseries_layout.addRow("Titel:", self.title_edit)

        settings_layout.addWidget(self.timeseries_group)

        # Abweichungsdiagramm-Parameter
        self.variance_group = QGroupBox("Abweichungsdiagramm-Parameter")
        variance_layout = QFormLayout(self.variance_group)

        self.key_column_edit = QLineEdit("Monat")
        self.actual_column_edit = QLineEdit("Umsatz_ist")
        self.plan_column_edit = QLineEdit("Umsatz_plan")
        self.var_column_edit = QLineEdit("Umsatz_var")
        self.var_title_edit = QLineEdit("Plan-Ist-Vergleich")

        variance_layout.addRow("Schlüsselspalte:", self.key_column_edit)
        variance_layout.addRow("Ist-Spalte:", self.actual_column_edit)
        variance_layout.addRow("Plan-Spalte:", self.plan_column_edit)
        variance_layout.addRow("Abweichungsspalte:", self.var_column_edit)
        variance_layout.addRow("Titel:", self.var_title_edit)

        settings_layout.addWidget(self.variance_group)

        # Diagrammerstellung-Button
        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Diagramm erstellen")
        self.create_button.clicked.connect(self.create_selected_chart)
        button_layout.addStretch()
        button_layout.addWidget(self.create_button)

        # Diagrammanzeige
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)

        # Alles zusammenfügen
        layout.addLayout(settings_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)

        # Standardeinstellung: Zeitreihendiagramm anzeigen, Abweichungsdiagramm ausblenden
        self.variance_group.setVisible(False)

    def on_chart_type_changed(self, index):
        """Wird aufgerufen, wenn der Diagrammtyp geändert wird"""
        if index == 0:  # Zeitreihendiagramm
            self.timeseries_group.setVisible(True)
            self.variance_group.setVisible(False)
        elif index == 1:  # Abweichungsdiagramm
            self.timeseries_group.setVisible(False)
            self.variance_group.setVisible(True)

    def set_data_sources(self, data_keys):
        """Setzt die verfügbaren Datensätze"""
        self.data_sources = data_keys

        # Aktuellen Text speichern
        current_data = self.data_combo.currentText()

        # Combobox leeren und neu füllen
        self.data_combo.clear()
        self.data_combo.addItems(data_keys)

        # Wenn möglich, vorherige Auswahl wiederherstellen
        if current_data in data_keys:
            self.data_combo.setCurrentText(current_data)

    def create_selected_chart(self):
        """Erstellt das ausgewählte Diagramm"""
        data_key = self.data_combo.currentText()

        if not data_key:
            return

        chart_index = self.chart_combo.currentIndex()

        if chart_index == 0:  # Zeitreihendiagramm
            chart_type = "time_series"
            parameters = {
                "x_col": self.x_col_edit.text(),
                "y_col": self.y_col_edit.text(),
                "title": self.title_edit.text()
            }
        elif chart_index == 1:  # Abweichungsdiagramm
            chart_type = "variance"
            parameters = {
                "key_column": self.key_column_edit.text(),
                "actual_column": self.actual_column_edit.text(),
                "plan_column": self.plan_column_edit.text(),
                "var_column": self.var_column_edit.text(),
                "title": self.var_title_edit.text()
            }
        else:
            return

        # Signal emittieren
        self.create_chart.emit(data_key, chart_type, parameters)

    def show_chart(self, figure):
        """Zeigt das Diagramm an"""
        if figure:
            # Alte Achsen löschen
            self.figure.clear()

            # Neue Achsen erstellen
            axes = self.figure.add_subplot(111)

            # Daten aus der übergebenen Figur kopieren
            for ax in figure.get_axes():
                # Linien kopieren
                for line in ax.get_lines():
                    axes.plot(line.get_xdata(), line.get_ydata(),
                              color=line.get_color(),
                              linestyle=line.get_linestyle(),
                              marker=line.get_marker(),
                              label=line.get_label())

                # Balken kopieren
                for container in ax.containers:
                    if hasattr(container, 'patches'):  # Für BarContainer
                        for i, patch in enumerate(container.patches):
                            axes.bar(i, patch.get_height(), color=patch.get_facecolor())

                # Titel und Achsenbeschriftungen kopieren
                if ax.get_title():
                    axes.set_title(ax.get_title())

                if ax.get_xlabel():
                    axes.set_xlabel(ax.get_xlabel())

                if ax.get_ylabel():
                    axes.set_ylabel(ax.get_ylabel())

                # Legende kopieren
                if ax.get_legend():
                    axes.legend()

            # Anzeige aktualisieren
            self.canvas.draw()