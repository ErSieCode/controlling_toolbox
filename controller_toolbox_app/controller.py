from PyQt6.QtWidgets import QMessageBox
from gui.main_window import MainWindow
from backend.controller_toolbox import ControllerToolbox
from data.data_manager import DataManager
import os
import pandas as pd


class ControllerApp:
    """Hauptklasse der Anwendung, die GUI und Backend verbindet"""

    def __init__(self):
        # Initialisierung der drei Schichten
        self.toolbox = ControllerToolbox()  # Anwendungslogik
        self.data_manager = DataManager()  # Datenhaltung
        self.main_window = MainWindow()  # GUI

        # Session-Daten
        self.session_data = {}
        self.dataframes = {}

        # Verbindungen herstellen
        self.connect_signals()

    def connect_signals(self):
        """Verbindet die GUI-Signale mit den Controller-Methoden"""
        # Datenimport-Signale
        self.main_window.import_tab.file_selected.connect(self.on_file_selected)
        self.main_window.import_tab.import_data.connect(self.on_import_data)

        # Analyse-Signale
        self.main_window.analysis_tab.run_analysis.connect(self.on_run_analysis)

        # Visualisierungs-Signale
        self.main_window.visualization_tab.create_chart.connect(self.on_create_chart)

        # Reporting-Signale
        self.main_window.reporting_tab.generate_report.connect(self.on_generate_report)

    def on_file_selected(self, file_path):
        """Wird aufgerufen, wenn eine Datei ausgewählt wird"""
        try:
            # Tabellenblätter ermitteln
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names

            # Tabellenblätter in der GUI aktualisieren
            self.main_window.import_tab.set_sheets(sheet_names)
        except Exception as e:
            self.main_window.show_error("Fehler beim Laden der Datei", str(e))

    def on_import_data(self, file_path, sheet_name, options):
        """Wird aufgerufen, wenn Daten importiert werden sollen"""
        try:
            # Daten laden
            df = self.toolbox.load_excel(file_path, sheet_name, **options)

            # Daten in Session speichern
            file_key = os.path.basename(file_path).split('.')[0]
            self.dataframes[file_key] = df

            # Vorschau aktualisieren
            self.main_window.import_tab.update_preview(df)

            # Verfügbare Datensätze in allen Tabs aktualisieren
            self.update_data_sources()

            # Erfolgsmeldung
            self.main_window.show_status(f"Daten aus '{file_path}' erfolgreich geladen")
        except Exception as e:
            self.main_window.show_error("Fehler beim Importieren der Daten", str(e))

    def update_data_sources(self):
        """Aktualisiert die verfügbaren Datensätze in allen Tabs"""
        data_keys = list(self.dataframes.keys())
        self.main_window.analysis_tab.set_data_sources(data_keys)
        self.main_window.visualization_tab.set_data_sources(data_keys)
        self.main_window.reporting_tab.set_data_sources(data_keys)

    def on_run_analysis(self, data_key, analysis_type, parameters):
        """Führt eine Analyse durch"""
        try:
            # Daten abrufen
            df = self.dataframes.get(data_key)
            if df is None:
                raise ValueError(f"Datensatz '{data_key}' nicht gefunden")

            # Analyse durchführen
            if analysis_type == "kpi":
                result = self.toolbox.calculate_kpis(df, **parameters)
            elif analysis_type == "variance":
                plan_key = parameters.pop("plan_data_key")
                plan_df = self.dataframes.get(plan_key)
                if plan_df is None:
                    raise ValueError(f"Plan-Datensatz '{plan_key}' nicht gefunden")
                result = self.toolbox.variance_analysis(df, plan_df, **parameters)
            else:
                raise ValueError(f"Unbekannter Analysetyp: {analysis_type}")

            # Ergebnis speichern
            result_key = f"{data_key}_{analysis_type}"
            self.dataframes[result_key] = result

            # Ergebnis anzeigen
            self.main_window.analysis_tab.show_result(result)

            # Datensätze aktualisieren
            self.update_data_sources()
        except Exception as e:
            self.main_window.show_error("Analysefehler", str(e))

    def on_create_chart(self, data_key, chart_type, parameters):
        """Erstellt ein Diagramm"""
        try:
            # Daten abrufen
            df = self.dataframes.get(data_key)
            if df is None:
                raise ValueError(f"Datensatz '{data_key}' nicht gefunden")

            # Diagramm erstellen
            if chart_type == "time_series":
                fig = self.toolbox.plot_time_series(df, **parameters)
            elif chart_type == "variance":
                fig = self.toolbox.plot_variance(df, **parameters)
            else:
                raise ValueError(f"Unbekannter Diagrammtyp: {chart_type}")

            # Diagramm anzeigen
            self.main_window.visualization_tab.show_chart(fig)
        except Exception as e:
            self.main_window.show_error("Visualisierungsfehler", str(e))

    def on_generate_report(self, config):
        """Generiert einen Bericht"""
        try:
            # Daten für den Bericht sammeln
            data_dict = {}
            for sheet_name, data_key in config["data_mapping"].items():
                df = self.dataframes.get(data_key)
                if df is None:
                    raise ValueError(f"Datensatz '{data_key}' nicht gefunden")
                data_dict[sheet_name] = df

            # Bericht erstellen
            report_path = self.toolbox.create_excel_report(
                data_dict,
                template_path=config.get("template_path"),
                output_path=config.get("output_path")
            )

            # Erfolgsmeldung
            self.main_window.show_status(f"Bericht erstellt: {report_path}")

            # Bericht anzeigen
            self.main_window.reporting_tab.show_report_info(report_path)
        except Exception as e:
            self.main_window.show_error("Berichtsfehler", str(e))