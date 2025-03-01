from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QGroupBox, QFormLayout, QLineEdit,
                             QTextEdit, QFileDialog)
from PyQt6.QtCore import pyqtSignal
import os


class ReportingTab(QWidget):
    """Tab für die Berichtserstellung"""

    # Signal für Kommunikation mit Controller
    generate_report = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_sources = []
        self.init_ui()

    def init_ui(self):
        """Initialisiert die UI-Komponenten"""
        layout = QVBoxLayout(self)

        # Berichtseinstellungen
        settings_group = QGroupBox("Berichtseinstellungen")
        settings_layout = QFormLayout(settings_group)

        # Vorlage auswählen
        template_layout = QHBoxLayout()
        self.template_edit = QLineEdit()
        self.template_edit.setPlaceholderText("Optional: Pfad zur Excel-Vorlage")
        self.template_browse_button = QPushButton("Durchsuchen...")
        self.template_browse_button.clicked.connect(self.browse_template)
        template_layout.addWidget(self.template_edit)
        template_layout.addWidget(self.template_browse_button)

        settings_layout.addRow("Berichtsvorlage:", template_layout)

        # Ausgabedatei
        output_layout = QHBoxLayout()
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("Pfad zur Ausgabedatei")
        self.output_browse_button = QPushButton("Durchsuchen...")
        self.output_browse_button.clicked.connect(self.browse_output)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.output_browse_button)

        settings_layout.addRow("Ausgabedatei:", output_layout)

        # Daten-Mapping
        mapping_group = QGroupBox("Daten-Mapping")
        mapping_layout = QVBoxLayout(mapping_group)

        self.mapping_text = QTextEdit()
        self.mapping_text.setPlaceholderText(
            "Tabellenblatt=Datensatz\n"
            "Beispiel:\n"
            "Umsatz=umsatzdaten\n"
            "Kosten=kostendaten\n"
            "Abweichung=umsatzdaten_variance"
        )
        mapping_layout.addWidget(self.mapping_text)

        # Verfügbare Datensätze anzeigen
        self.available_datasets_label = QLabel("Verfügbare Datensätze: Keine")
        mapping_layout.addWidget(self.available_datasets_label)

        # Berichtsgenerierung
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Bericht generieren")
        self.generate_button.clicked.connect(self.generate_selected_report)
        button_layout.addStretch()
        button_layout.addWidget(self.generate_button)

        # Berichtsinformation
        info_group = QGroupBox("Berichtsinformation")
        info_layout = QVBoxLayout(info_group)

        self.info_label = QLabel("Kein Bericht generiert")
        self.open_button = QPushButton("Bericht öffnen")
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(self.open_report)

        info_layout.addWidget(self.info_label)
        info_layout.addWidget(self.open_button)

        # Alles zusammenfügen
        layout.addWidget(settings_group)
        layout.addWidget(mapping_group)
        layout.addLayout(button_layout)
        layout.addWidget(info_group)

    def browse_template(self):
        """Öffnet einen Datei-Browser-Dialog für die Vorlage"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Excel-Vorlage öffnen",
            "",
            "Excel-Dateien (*.xlsx *.xls *.xlsm)"
        )

        if file_path:
            self.template_edit.setText(file_path)

    def browse_output(self):
        """Öffnet einen Datei-Browser-Dialog für die Ausgabedatei"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Bericht speichern unter",
            "",
            "Excel-Dateien (*.xlsx)"
        )

        if file_path:
            if not file_path.lower().endswith('.xlsx'):
                file_path += '.xlsx'
            self.output_edit.setText(file_path)

    def set_data_sources(self, data_keys):
        """Setzt die verfügbaren Datensätze"""
        self.data_sources = data_keys

        # Verfügbare Datensätze anzeigen
        if data_keys:
            datasets_text = "Verfügbare Datensätze: " + ", ".join(data_keys)
        else:
            datasets_text = "Verfügbare Datensätze: Keine"

        self.available_datasets_label.setText(datasets_text)

    def generate_selected_report(self):
        """Generiert den konfigurierten Bericht"""
        # Vorlage und Ausgabepfad
        template_path = self.template_edit.text() if self.template_edit.text() else None
        output_path = self.output_edit.text() if self.output_edit.text() else None

        # Mapping aus Text extrahieren
        mapping_text = self.mapping_text.toPlainText()
        data_mapping = {}

        for line in mapping_text.strip().split('\n'):
            if '=' in line:
                sheet, dataset = line.split('=', 1)
                sheet = sheet.strip()
                dataset = dataset.strip()

                if dataset in self.data_sources:
                    data_mapping[sheet] = dataset

        if not data_mapping:
            self.info_label.setText("Fehler: Kein gültiges Daten-Mapping angegeben")
            return

        # Konfiguration erstellen
        config = {
            "template_path": template_path,
            "output_path": output_path,
            "data_mapping": data_mapping
        }

        # Signal emittieren
        self.generate_report.emit(config)

    def show_report_info(self, report_path):
        """Zeigt Informationen zum generierten Bericht an"""
        if report_path and os.path.exists(report_path):
            self.info_label.setText(f"Bericht wurde erstellt: {report_path}")
            self.open_button.setEnabled(True)
            self.report_path = report_path
        else:
            self.info_label.setText("Fehler beim Erstellen des Berichts")
            self.open_button.setEnabled(False)

    def open_report(self):
        """Öffnet den generierten Bericht"""
        if hasattr(self, 'report_path') and os.path.exists(self.report_path):
            import subprocess
            import sys

            if sys.platform == 'win32':
                os.startfile(self.report_path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', self.report_path], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', self.report_path], check=True)