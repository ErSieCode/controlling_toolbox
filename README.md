# Controller Toolbox - Dokumentation der Python-Anwendung

![Controller Toolbox Screenshot](https://github.com/ErSieCode/controlling_toolbox/blob/main/controller_toolbox_first_look.jpg)

## 1. Überblick und Zielsetzung

Die Controller Toolbox ist eine moderne Python-Desktopanwendung, die speziell für Controlling-Aufgaben entwickelt wurde. Sie bietet umfassende Funktionen zur Excel-basierten Datenanalyse, Berichterstellung und Visualisierung in einer intuitiven Benutzeroberfläche. Die Anwendung richtet sich an Controller und Finanzanalysten, die regelmäßig mit Excel-Daten arbeiten und fortgeschrittene Analysen durchführen.

### Kernfunktionalitäten:
- Import und Aufbereitung von Excel-Daten
- Berechnung relevanter Finanzkennzahlen (KPIs)
- Plan-Ist-Vergleiche und Abweichungsanalysen
- Erstellung von Prognosen und Forecasts
- Professionelle Visualisierung von Daten
- Automatisierte Berichterstellung
- Dashboard mit Echtzeit-KPIs

## 2. Technische Grundlagen

### Verwendete Technologien

#### Backend
- **Python 3.7+**: Grundlegende Programmiersprache
- **Pandas/NumPy**: Datenverarbeitung und -analyse
- **Matplotlib/Seaborn**: Datenvisualisierung
- **Openpyxl**: Excel-Operationen
- **SQLite/SQLAlchemy**: Lokale Datenspeicherung
- **Statsmodels/SciPy**: Statistische Analysen und Prognosen

#### Frontend (GUI)
- **PyQt6/PySide6**: Framework für die grafische Benutzeroberfläche
- **Qt Designer**: Tool für das visuelle UI-Design
- **Matplotlib Qt Backend**: Integration von Diagrammen in die GUI

## 3. Systemarchitektur

Die Controller Toolbox folgt einer klassischen Drei-Schichten-Architektur:

### Präsentationsschicht (GUI)
Enthält alle UI-Komponenten und ist für die Darstellung und Benutzerinteraktion verantwortlich.
- **MainWindow**: Hauptfenster mit Tab-Navigation
- **Spezialisierte Tabs**: Module für verschiedene Funktionen (Import, Analyse, etc.)
- **Dialoge und Forms**: Eingabeformulare und Hilfsdialoge

### Anwendungslogik (Business Logic)
Verarbeitet Benutzeranfragen, führt Berechnungen durch und orchestriert Prozesse.
- **ControllerToolbox**: Zentrales Backend-Modul mit fachlichen Funktionen
- **Spezialisierte Module**: Für Datenanalyse, Visualisierung, etc.

### Datenhaltung (Data Access)
Verantwortlich für Datenpersistenz, Laden und Speichern.
- **DataManager**: Verwaltung von Datensätzen und Einstellungen
- **SQLite-Datenbank**: Speicherung von Metadaten, Einstellungen, etc.
- **Excel-Dateien**: Externe Datenquellen und Berichtsziele

### Kommunikation zwischen den Schichten
Die Schichten kommunizieren über definierte Schnittstellen:
- **Signals und Slots**: Für die Kommunikation zwischen GUI und Logik
- **Methoden mit definierten Parametern**: Für den Aufruf von Geschäftslogik
- **Datenmodelle**: Für den Austausch zwischen den Schichten

## 4. Komponentenübersicht

### 4.1 Hauptanwendung (`ControllerApp`)

Die Hauptklasse `ControllerApp` initialisiert die Anwendung und verbindet die drei Schichten:

```python
class ControllerApp:
    def __init__(self):
        # Initialisierung der drei Schichten
        self.toolbox = ControllerToolbox()       # Anwendungslogik
        self.data_manager = DataManager()        # Datenhaltung
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()          # GUI

        # Session-Daten
        self.session_data = {}
        self.dataframes = {}
        
        # Verbindungen herstellen
        self.connect_signals()
    
    def run(self):
        """Startet die Anwendung"""
        self.main_window.show()
        return self.app.exec()
```

### 4.2 GUI-Komponenten

#### MainWindow
Das Hauptfenster der Anwendung enthält:
- Menüleiste
- Symbolleiste
- Tab-Widget mit verschiedenen Funktionsbereichen
- Statusleiste

```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controller Toolbox")
        self.setMinimumSize(1200, 800)
        
        # Zentrale Widget-Struktur
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        # Tabs für verschiedene Funktionen
        self.dashboard_tab = DashboardTab()
        self.import_tab = ImportTab()
        self.analysis_tab = AnalysisTab()
        self.visualization_tab = VisualizationTab()
        self.reporting_tab = ReportingTab()
        self.forecasting_tab = ForecastingTab()
        
        # Tabs hinzufügen
        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        self.tab_widget.addTab(self.import_tab, "Datenimport")
        self.tab_widget.addTab(self.analysis_tab, "Analyse")
        # ...
```

#### Spezialisierte Tabs
Jeder Tab wird als separate Klasse implementiert:

**DashboardTab**: Zeigt eine Übersicht der wichtigsten KPIs und Charts.

**ImportTab**: Ermöglicht den Import von Excel-Dateien:
```python
class ImportTab(QWidget):
    # Signale für Kommunikation mit Controller
    file_selected = pyqtSignal(str)
    import_data = pyqtSignal(str, str, dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        # UI-Elemente für Dateiauswahl, Tabellenblatt-Auswahl,
        # Datenvorschau, etc.
```

**AnalysisTab**: Bietet Datenanalyse-Funktionen:
```python
class AnalysisTab(QWidget):
    # Signale
    run_analysis = pyqtSignal(str, str, dict)  # data_key, analysis_type, parameters
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        # UI-Elemente für Datenauswahl, Analyse-Optionen,
        # Ergebnisanzeige, etc.
```

**VisualizationTab**: Bietet Funktionen zur Diagrammerstellung:
```python
class VisualizationTab(QWidget):
    # Signale
    create_chart = pyqtSignal(str, str, dict)  # data_key, chart_type, options
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        # UI-Elemente für Diagrammtyp-Auswahl, Konfiguration,
        # Vorschau, etc.
```

**ReportingTab**: Ermöglicht die Erstellung von Berichten:
```python
class ReportingTab(QWidget):
    # Signale
    generate_report = pyqtSignal(dict)  # report_config
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        # UI-Elemente für Berichtsvorlagen, -konfiguration,
        # Vorschau, etc.
```

**ForecastingTab**: Bietet Prognose-Funktionen:
```python
class ForecastingTab(QWidget):
    # Signale
    create_forecast = pyqtSignal(str, str, str, str, int, dict)  # data_key, time_col, value_col, method, periods, options
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        # UI-Elemente für Datenauswahl, Prognosemethode,
        # Parameter, Ergebnisanzeige, etc.
```

### 4.3 Backend-Komponenten (Anwendungslogik)

#### ControllerToolbox
Die Hauptklasse im Backend, die alle Controlling-Funktionen enthält:

```python
class ControllerToolbox:
    def __init__(self):
        self.data = None
        self.report_date = dt.datetime.now().strftime("%Y-%m-%d")
    
    # Daten-Import/-Export
    def load_excel(self, filepath, sheet_name=0, skiprows=None, usecols=None):
        """Lädt Daten aus einer Excel-Datei"""
        
    def save_to_excel(self, df, filepath, sheet_name="Report", index=True, autoformat=False):
        """Speichert Daten in eine Excel-Datei"""
    
    # Datenaufbereitung
    def clean_data(self, df=None):
        """Bereinigt Daten (Entfernt Duplikate, behandelt NaN-Werte)"""
    
    def convert_column_types(self, df=None, type_dict=None):
        """Konvertiert Spaltentypen"""
    
    # Kennzahlenberechnung
    def calculate_kpis(self, df=None, revenue_col='Umsatz', cost_col='Kosten', time_col='Datum'):
        """Berechnet Finanzkennzahlen"""
    
    def calculate_financial_ratios(self, df=None):
        """Berechnet Finanzkennzahlen aus Bilanz und GuV"""
    
    # Abweichungsanalyse
    def variance_analysis(self, actual_df, plan_df, key_column, value_columns=None):
        """Führt eine Abweichungsanalyse zwischen Ist- und Plandaten durch"""
    
    # Prognose
    def create_forecast(self, df=None, time_col='Datum', value_col='Wert', periods=12, method='ets'):
        """Erstellt eine Zeitreihenprognose"""
    
    # Visualisierung
    def plot_time_series(self, df=None, x_col='Datum', y_col='Wert', title='Zeitreihenanalyse'):
        """Erstellt ein Zeitreihendiagramm"""
    
    def plot_variance(self, variance_df, key_column, actual_column, plan_column, var_column):
        """Erstellt ein Diagramm zur Abweichungsanalyse"""
    
    # Reporting
    def create_monthly_report(self, data_dict, month=None, year=None, template=None, output_file=None):
        """Erstellt einen monatlichen Controlling-Bericht"""
```

### 4.4 Datenhaltungskomponenten

#### DataManager
Verantwortlich für die Speicherung und Verwaltung von Daten:

```python
class DataManager:
    def __init__(self, db_path=None):
        # Pfad zur SQLite-Datenbank
        if db_path is None:
            app_dir = Path.home() / ".controller_toolbox"
            app_dir.mkdir(exist_ok=True)
            db_path = app_dir / "controller_data.db"
        
        self.db_path = str(db_path)
        self.conn = None
        self.init_db()
    
    def init_db(self):
        """Initialisiert die Datenbank-Tabellen"""
    
    def save_setting(self, key, value):
        """Speichert eine Anwendungseinstellung"""
    
    def get_setting(self, key, default=None):
        """Liest eine Anwendungseinstellung"""
    
    def register_dataset(self, name, description, file_path):
        """Registriert einen Datensatz in der Datenbank"""
    
    def get_datasets(self):
        """Gibt alle registrierten Datensätze zurück"""
    
    def save_dataframe(self, df, file_path, sheet_name="Sheet1", index=True):
        """Speichert einen DataFrame in eine Excel-Datei"""
    
    def load_dataframe(self, file_path, sheet_name=0):
        """Lädt einen DataFrame aus einer Excel-Datei"""
```

## 5. Implementierungsanleitung

### 5.1 Voraussetzungen

1. **Software-Installation**:
   - Python 3.7 oder höher
   - Git (optional, für Versionskontrolle)
   - Visual Studio Code oder PyCharm (empfohlen)

2. **Python-Umgebung einrichten**:
   ```bash
   # Virtuelle Umgebung erstellen
   python -m venv controller_env
   
   # Unter Windows aktivieren
   controller_env\Scripts\activate
   
   # Unter Linux/Mac aktivieren
   source controller_env/bin/activate
   
   # Abhängigkeiten installieren
   pip install pandas numpy matplotlib seaborn openpyxl scipy statsmodels PyQt6 PyQt6-tools SQLAlchemy
   ```

### 5.2 Projektstruktur anlegen

Erstellen Sie folgende Verzeichnisstruktur:

```
controller_toolbox_app/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Einstiegspunkt
│   ├── controller.py            # Controller-Klasse
│   ├── gui/                     # GUI-Komponenten
│   ├── backend/                 # Anwendungslogik
│   ├── data/                    # Datenhaltung
│   ├── resources/               # Ressourcen (Icons, etc.)
│   └── utils/                   # Hilfsfunktionen
├── tests/                       # Testfälle
├── docs/                        # Dokumentation
├── setup.py                     # Installation
└── requirements.txt             # Abhängigkeiten
```

### 5.3 Implementierungsschritte

#### Schritt 1: Implementierung der Datenhaltung

Erstellen Sie zuerst die Datenhaltungsschicht:

1. Implementieren Sie `app/data/data_manager.py` mit dem `DataManager`
2. Testen Sie grundlegende Funktionen: Datenbankverbindung, Einstellungen speichern/laden

#### Schritt 2: Implementierung der Anwendungslogik

Implementieren Sie die Kernfunktionalität:

1. Erstellen Sie `app/backend/controller_toolbox.py` mit dem `ControllerToolbox`
2. Implementieren Sie die Module für die verschiedenen Funktionsbereiche:
   - `data_handling.py`: Daten-Import/-Export
   - `data_processing.py`: Datenbereinigung
   - `financial_analysis.py`: Kennzahlenberechnung
   - `forecasting.py`: Prognose-Funktionen
   - `visualization.py`: Diagramm-Funktionen
   - `reporting.py`: Berichterstattungs-Funktionen

3. Testen Sie jede Funktion mit Beispieldaten

#### Schritt 3: Implementierung der GUI

Erstellen Sie die Benutzeroberfläche:

1. Implementieren Sie `app/gui/main_window.py` mit dem Hauptfenster
2. Implementieren Sie die verschiedenen Tabs als separate Module:
   - `dashboard_tab.py`: Dashboard
   - `import_tab.py`: Datenimport
   - `analysis_tab.py`: Analyse
   - `visualization_tab.py`: Visualisierung
   - `reporting_tab.py`: Reporting
   - `forecasting_tab.py`: Prognose

3. Erstellen Sie benötigte Dialoge und Hilfswidgets

#### Schritt 4: Implementierung der Controller-Klasse

1. Implementieren Sie `app/controller.py` mit der `ControllerApp`-Klasse
2. Verbinden Sie die GUI-Signale mit der Anwendungslogik
3. Implementieren Sie die Session-Verwaltung

#### Schritt 5: Hauptmodul und Anwendungsstart 

1. Implementieren Sie `app/main.py` als Einstiegspunkt
2. Testen Sie den Anwendungsstart

## 6. Code-Beispiele für zentrale Funktionen

### 6.1 Anwendungsstart (main.py)

```python
import sys
from app.controller import ControllerApp

def main():
    """Haupteinstiegspunkt der Anwendung"""
    controller = ControllerApp()
    return controller.run()

if __name__ == "__main__":
    sys.exit(main())
```

### 6.2 Daten importieren und visualisieren

```python
# Beispiel für eine typische Nutzung der Controller Toolbox
from app.backend.controller_toolbox import ControllerToolbox

# Controller Toolbox initialisieren
ct = ControllerToolbox()

# Daten laden
excel_data = ct.load_excel("umsatzdaten.xlsx", sheet_name="2025")

# Daten bereinigen
clean_data = ct.clean_data(excel_data)

# Kennzahlen berechnen
kpi_data = ct.calculate_kpis(clean_data, 
                             revenue_col="Umsatz", 
                             cost_col="Kosten", 
                             time_col="Datum")

# Visualisierung erstellen
fig = ct.plot_time_series(kpi_data, 
                         x_col="Datum", 
                         y_col="Deckungsbeitrag", 
                         title="Deckungsbeitrag im Zeitverlauf")

# Daten exportieren
ct.save_to_excel(kpi_data, "kpi_analyse.xlsx", autoformat=True)
```

### 6.3 Plan-Ist-Vergleich durchführen

```python
# Plan-Daten laden
plan_data = ct.load_excel("plandaten.xlsx", sheet_name="2025_Budget")

# Ist-Daten laden und bereinigen
actual_data = ct.load_excel("istdaten.xlsx")
actual_data = ct.clean_data(actual_data)

# Abweichungsanalyse durchführen
variance = ct.variance_analysis(actual_data, plan_data, 
                               key_column="Monat", 
                               value_columns=["Umsatz", "Kosten", "DB"])

# Visualisierung der Abweichung
fig = ct.plot_variance(variance, 
                      key_column="Monat",
                      actual_column="Umsatz_ist",
                      plan_column="Umsatz_plan",
                      var_column="Umsatz_var")

# Bericht erstellen
ct.create_monthly_report(
    data_dict={
        "variance": variance,
        "actual": actual_data,
        "plan": plan_data,
        "charts": [fig]
    },
    month=3,
    year=2025,
    output_file="Abweichungsanalyse_März_2025.xlsx"
)
```

### 6.4 Signal-Slot-Verbindung im Controller

```python
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
    
    # Prognose-Signale
    self.main_window.forecasting_tab.create_forecast.connect(self.on_create_forecast)

def on_file_selected(self, file_path):
    """Wird aufgerufen, wenn eine Datei ausgewählt wird"""
    try:
        # Tabellenblätter ermitteln
        import pandas as pd
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
```

## 7. Benutzeroberfläche im Detail

### 7.1 Dashboard-Tab

Das Dashboard bietet einen schnellen Überblick über die wichtigsten KPIs und Trends:

- **KPI-Karten**: Zeigen Schlüsselkennzahlen mit Veränderungen
- **Hauptcharts**: Visualisieren wichtige Zeitreihen und Verteilungen
- **Tabellen**: Listen der Top-Produkte und größten Abweichungen

```python
def create_kpi_card(self, title, value, change):
    """Erstellt eine KPI-Karte für das Dashboard"""
    card = QGroupBox(title)
    layout = QVBoxLayout(card)
    
    value_label = QLabel(value)
    value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
    value_label.setAlignment(Qt.AlignCenter)
    
    change_label = QLabel(change)
    if change.startswith('+'):
        change_label.setStyleSheet("color: green; font-weight: bold;")
    elif change.startswith('-'):
        change_label.setStyleSheet("color: red; font-weight: bold;")
    change_label.setAlignment(Qt.AlignCenter)
    
    layout.addWidget(value_label)
    layout.addWidget(change_label)
    
    return card
```

### 7.2 Datenimport-Tab

Der Datenimport-Tab ermöglicht das Laden und Voranzeigen von Excel-Dateien:

- **Dateiauswahl**: Über Dialog oder direkten Pfad
- **Tabellenblattauswahl**: Dropdown mit verfügbaren Blättern
- **Vorschau**: Tabellendarstellung der Daten
- **Importoptionen**: Spaltenauswahl, Zeilenüberspringen, etc.

### 7.3 Analyse-Tab

Der Analyse-Tab bietet verschiedene Analysefunktionen:

- **Datenauswahl**: Dropdown mit verfügbaren Datensätzen
- **Funktionsauswahl**: Verschiedene Analyseoptionen
- **Konfiguration**: Parameter für die jeweilige Funktion
- **Ergebnisvorschau**: Tabelle mit Analyseergebnissen

### 7.4 Visualisierungs-Tab

Der Visualisierungs-Tab ermöglicht die Erstellung verschiedener Diagramme:

- **Diagrammtyp**: Auswahl des gewünschten Visualisierungstyps
- **Datenauswahl**: Datensatz und Spalten für X/Y-Achsen
- **Optionen**: Titel, Beschriftungen, Farben, etc.
- **Vorschau**: Interaktive Diagrammanzeige
- **Export**: Speicherung als Bild oder in Berichte

### 7.5 Reporting-Tab

Der Reporting-Tab dient zur Erstellung von Berichten:

- **Vorlagenauswahl**: Vordefinierte oder benutzerdefinierte Berichtsvorlagen
- **Elementkonfiguration**: Auswahl und Anordnung von Berichtselementen
- **Berichtsoptionen**: Titel, Datum, Autor, etc.
- **Vorschau**: HTML-Vorschau des generierten Berichts
- **Export**: Speicherung als Excel oder PDF

### 7.6 Prognose-Tab

Der Prognose-Tab ermöglicht die Erstellung von Zeitreihenprognosen:

- **Datenauswahl**: Zeitreihen-Daten und relevante Spalten
- **Methodenauswahl**: Verschiedene Prognosemethoden (ETS, ARIMA, etc.)
- **Parameter**: Konfiguration der Prognosemethode
- **Ergebnis**: Diagramm und Tabelle mit Prognosewerten

## 8. Anwendung ausführen und verteilen

### 8.1 Während der Entwicklung ausführen

```bash
# Im Projektverzeichnis
cd controller_toolbox_app

# Virtuelle Umgebung aktivieren
source controller_env/bin/activate  # Linux/Mac
# oder
controller_env\Scripts\activate  # Windows

# Anwendung starten
python -m app.main
```

### 8.2 Als eigenständige Anwendung verteilen

Für die Distribution als eigenständige Anwendung kann PyInstaller verwendet werden:

```bash
# PyInstaller installieren
pip install pyinstaller

# Anwendung verpacken
pyinstaller --name="ControllerToolbox" --windowed --onefile app/main.py

# Die ausführbare Datei wird im dist/-Verzeichnis erstellt
```

Alternativ können Sie auch installierbare Pakete erstellen:

```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="controller_toolbox",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "openpyxl>=3.0.0",
        "PyQt6>=6.1.0",
        "scipy>=1.7.0",
        "statsmodels>=0.12.0",
        "SQLAlchemy>=1.4.0"
    ],
    entry_points={
        'console_scripts': [
            'controller_toolbox=app.main:main',
        ],
    },
    python_requires=">=3.7",
)
```

## 9. Fehlerbehandlung und Logging

Die Anwendung sollte ein robustes Fehlerbehandlungssystem implementieren:

```python
# app/utils/logger.py
import logging
import os
from pathlib import Path

def setup_logger():
    """Richtet das Logging-System ein"""
    # Log-Verzeichnis
    log_dir = Path.home() / ".controller_toolbox" / "logs"
    log_dir.mkdir(exist_ok=True, parents=True)
    
    # Logger konfigurieren
    logger = logging.getLogger("controller_toolbox")
    logger.setLevel(logging.DEBUG)
    
    # Datei-Handler
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setLevel(logging.DEBUG)
    
    # Konsolen-Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Handler hinzufügen
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger abrufen
logger = setup_logger()
```

## 10. Erweiterungsmöglichkeiten

Die Controller Toolbox kann je nach Bedarf erweitert werden:

1. **Integration mit Datenbanken**:
   - Anbindung an SQL-Datenbanken für große Datenmengen
   - Direkte Verbindung zu ERP-Systemen (SAP, etc.)

2. **KI/ML-Integration**:
   - Machine Learning für präzisere Prognosen
   - Anomalieerkennung für frühzeitige Warnungen

3. **Cloud-Integration**:
   - Datenspeicherung in der Cloud (OneDrive, Google Drive)
   - Berichtsfreigabe über Cloud-Dienste

4. **Collaboration-Features**:
   - Mehrbenutzer-Support
   - Kommentar- und Notizfunktionen

5. **API-Schnittstellen**:
   - Anbindung an Finanz-APIs
   - Import von Marktdaten

## 11. Zusammenfassung (Fortsetzung)

Die Implementierung folgt bewährten Software-Engineering-Praktiken:
- Klare Trennung von Benutzeroberfläche, Geschäftslogik und Datenhaltung
- Modularität durch spezialisierte Klassen und Funktionen
- Erweiterbarkeit durch konsistente Schnittstellen
- Robuste Fehlerbehandlung und Logging

## 12. Best Practices für die Implementierung

### 12.1 Code-Organisation

Für eine wartbare und übersichtliche Anwendung sollten Sie folgende Prinzipien beachten:

1. **Modularer Aufbau**: Jeder Funktionsbereich sollte in einem eigenen Modul implementiert werden
2. **Klare Verantwortlichkeiten**: Jede Klasse sollte eine klar definierte Aufgabe haben
3. **Wiederverwendbarer Code**: Gemeinsame Funktionalitäten in Hilfsfunktionen auslagern
4. **Konsistente Benennung**: Einheitliche Namenskonventionen für Klassen, Methoden und Variablen

### 12.2 Benutzeroberflächen-Design

Beachten Sie folgende Prinzipien für eine benutzerfreundliche GUI:

1. **Konsistenz**: Einheitliche Anordnung, Bezeichnungen und Aktionen
2. **Feedback**: Klare Rückmeldungen zu Benutzeraktionen
3. **Fehlerprävention**: Validierung von Eingaben, Bestätigungsdialoge für kritische Aktionen
4. **Effizienz**: Tastaturkürzel, Kontextmenüs und optimierte Arbeitsabläufe
5. **Ästhetik**: Ansprechendes Design mit ausreichend Abständen und konsistenten Farben

```python
# Beispiel für einen Bestätigungsdialog
def confirm_action(self, title, message):
    """Zeigt einen Bestätigungsdialog an und gibt True zurück, wenn der Benutzer bestätigt"""
    from PyQt6.QtWidgets import QMessageBox
    
    reply = QMessageBox.question(
        self, 
        title, 
        message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    
    return reply == QMessageBox.StandardButton.Yes
```

### 12.3 Multithreading

Für rechenintensive Operationen sollten Sie Multithreading verwenden, um das Einfrieren der Benutzeroberfläche zu vermeiden:

```python
from PyQt6.QtCore import QThread, pyqtSignal

class AnalysisWorker(QThread):
    """Worker-Thread für rechenintensive Analysen"""
    finished = pyqtSignal(object)  # Signal mit Ergebnis
    error = pyqtSignal(str)        # Signal für Fehler
    
    def __init__(self, function, args=None, kwargs=None):
        super().__init__()
        self.function = function
        self.args = args or []
        self.kwargs = kwargs or {}
    
    def run(self):
        try:
            result = self.function(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

# Verwendung im Controller:
def on_run_analysis(self, data_key, analysis_type, params):
    """Führt eine Analyse in einem separaten Thread aus"""
    # Daten vorbereiten
    df = self.dataframes.get(data_key)
    if df is None:
        self.main_window.show_error("Fehler", f"Datensatz '{data_key}' nicht gefunden")
        return
    
    # Fortschrittsanzeige
    self.main_window.show_busy("Analyse wird durchgeführt...")
    
    # Funktion basierend auf Analysetyp auswählen
    if analysis_type == "clean_data":
        func = self.toolbox.clean_data
        kwargs = {}
    elif analysis_type == "calculate_kpis":
        func = self.toolbox.calculate_kpis
        kwargs = params
    else:
        self.main_window.show_error("Fehler", f"Unbekannter Analysetyp: {analysis_type}")
        return
    
    # Worker erstellen und verbinden
    self.worker = AnalysisWorker(func, [df], kwargs)
    self.worker.finished.connect(lambda result: self.on_analysis_finished(result, data_key, analysis_type))
    self.worker.error.connect(lambda error: self.on_analysis_error(error))
    
    # Thread starten
    self.worker.start()

def on_analysis_finished(self, result, data_key, analysis_type):
    """Wird aufgerufen, wenn die Analyse abgeschlossen ist"""
    # Fortschrittsanzeige ausblenden
    self.main_window.hide_busy()
    
    # Ergebnis in Session speichern
    result_key = f"{data_key}_{analysis_type}"
    self.dataframes[result_key] = result
    
    # GUI aktualisieren
    self.main_window.analysis_tab.show_result(result)
    self.main_window.show_status(f"Analyse '{analysis_type}' erfolgreich abgeschlossen")
    
    # Verfügbare Datensätze aktualisieren
    self.update_data_sources()

def on_analysis_error(self, error):
    """Wird aufgerufen, wenn bei der Analyse ein Fehler auftritt"""
    # Fortschrittsanzeige ausblenden
    self.main_window.hide_busy()
    
    # Fehlermeldung anzeigen
    self.main_window.show_error("Analysefehler", error)
```

### 12.4 Konfiguration und Einstellungen

Implementieren Sie ein flexibles Konfigurationssystem für Benutzereinstellungen:

```python
# app/utils/config.py
import json
import os
from pathlib import Path

class Config:
    """Klasse für Anwendungseinstellungen"""
    
    def __init__(self, config_file=None):
        """Initialisiert die Konfiguration"""
        # Standardpfad
        if config_file is None:
            app_dir = Path.home() / ".controller_toolbox"
            app_dir.mkdir(exist_ok=True)
            config_file = app_dir / "config.json"
        
        self.config_file = config_file
        self.config = self.load()
    
    def load(self):
        """Lädt die Konfiguration aus der Datei"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Fehler beim Laden der Konfiguration: {e}")
        
        # Standardkonfiguration
        return {
            "general": {
                "language": "de",
                "theme": "light",
                "recent_files": []
            },
            "import": {
                "default_sheet": 0,
                "preview_rows": 100
            },
            "analysis": {
                "default_kpis": ["Umsatz", "DB1", "Marge"]
            },
            "visualization": {
                "default_chart": "line",
                "color_scheme": "blue"
            },
            "reporting": {
                "default_template": "monthly_report",
                "company_name": "",
                "logo_path": ""
            }
        }
    
    def save(self):
        """Speichert die Konfiguration in der Datei"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")
            return False
    
    def get(self, section, key, default=None):
        """Liest einen Konfigurationswert"""
        return self.config.get(section, {}).get(key, default)
    
    def set(self, section, key, value):
        """Setzt einen Konfigurationswert"""
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
        return self.save()
    
    def add_recent_file(self, file_path):
        """Fügt eine Datei zur Liste der kürzlich verwendeten Dateien hinzu"""
        recent_files = self.get("general", "recent_files", [])
        
        # Datei entfernen, wenn bereits vorhanden
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # Am Anfang einfügen
        recent_files.insert(0, file_path)
        
        # Auf maximal 10 Einträge begrenzen
        recent_files = recent_files[:10]
        
        # Speichern
        self.set("general", "recent_files", recent_files)
```

## 13. Detaillierte Implementierung wichtiger Funktionen

### 13.1 Excel-Import mit Vorschau

Eine wichtige Funktion ist der Import von Excel-Dateien mit Vorschau:

```python
def load_excel_with_preview(self, file_path, sheet_name=0, max_rows=100):
    """
    Lädt eine Excel-Datei mit Vorschau der ersten Zeilen
    
    Args:
        file_path (str): Pfad zur Excel-Datei
        sheet_name: Name oder Index des Tabellenblatts
        max_rows (int): Maximale Anzahl der Zeilen für die Vorschau
    
    Returns:
        tuple: (DataFrame mit allen Daten, DataFrame mit Vorschaudaten)
    """
    try:
        # Dateiendung prüfen
        if not file_path.lower().endswith(('.xlsx', '.xls', '.xlsm')):
            raise ValueError("Die Datei ist keine Excel-Datei.")
        
        # Vorschau laden
        preview_df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=max_rows)
        
        # Vollständige Daten laden
        full_df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        return full_df, preview_df
    except Exception as e:
        raise Exception(f"Fehler beim Laden der Excel-Datei: {str(e)}")
```

### 13.2 Berichterstellung mit Excel-Templates

Eine zentrale Funktion für Controller ist die automatisierte Berichterstellung:

```python
def create_excel_report(self, data_dict, template_path=None, output_path=None):
    """
    Erstellt einen Excel-Bericht basierend auf einer Vorlage
    
    Args:
        data_dict (dict): Dictionary mit DataFrames für verschiedene Tabellenblätter
        template_path (str): Pfad zur Excel-Vorlage (optional)
        output_path (str): Pfad für die Ausgabedatei (optional)
    
    Returns:
        str: Pfad zur erstellten Berichtsdatei
    """
    from openpyxl import load_workbook
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl.chart import BarChart, Reference
    import os
    from datetime import datetime
    
    try:
        # Ausgabepfad generieren, falls nicht angegeben
        if output_path is None:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"Bericht_{now}.xlsx"
        
        # Vorlage laden oder neue Arbeitsmappe erstellen
        if template_path and os.path.exists(template_path):
            wb = load_workbook(template_path)
        else:
            from openpyxl import Workbook
            wb = Workbook()
            # Standardblatt umbenennen
            if "Sheet" in wb.sheetnames:
                wb["Sheet"].title = "Übersicht"
        
        # Für jeden DataFrame im Dictionary
        for sheet_name, df in data_dict.items():
            # Prüfen, ob das Tabellenblatt existiert
            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                # Bereich für Daten löschen (ab Zeile 2)
                for row in ws.iter_rows(min_row=2):
                    for cell in row:
                        cell.value = None
            else:
                # Neues Tabellenblatt erstellen
                ws = wb.create_sheet(title=sheet_name)
            
            # DataFrame in das Tabellenblatt schreiben
            for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
                for c_idx, value in enumerate(row, 1):
                    ws.cell(row=r_idx, column=c_idx, value=value)
            
            # Spaltenbreiten anpassen
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                
                adjusted_width = max(max_length + 2, 10)
                ws.column_dimensions[column].width = adjusted_width
            
            # Diagramm erstellen, wenn Daten geeignet sind
            if sheet_name.lower() in ["umsatz", "kosten", "deckungsbeitrag"] and len(df) > 0:
                if "Datum" in df.columns and any(col for col in df.columns if col != "Datum"):
                    value_col = next(col for col in df.columns if col != "Datum")
                    
                    # Diagramm erstellen
                    chart = BarChart()
                    chart.title = f"{sheet_name} nach Datum"
                    chart.x_axis.title = "Datum"
                    chart.y_axis.title = value_col
                    
                    # Datenbereich
                    data = Reference(ws, min_col=df.columns.get_loc(value_col) + 1, 
                                    min_row=1, max_row=len(df) + 1)
                    cats = Reference(ws, min_col=df.columns.get_loc("Datum") + 1, 
                                   min_row=2, max_row=len(df) + 1)
                    
                    chart.add_data(data, titles_from_data=True)
                    chart.set_categories(cats)
                    
                    # Diagramm positionieren
                    ws.add_chart(chart, "H2")
        
        # Arbeitsmappe speichern
        wb.save(output_path)
        return output_path
    
    except Exception as e:
        raise Exception(f"Fehler bei der Berichterstellung: {str(e)}")
```

### 13.3 Finanzielle Kennzahlenberechnung

Eine wichtige Funktion für Controller ist die Berechnung von Finanzkennzahlen:

```python
def calculate_kpis(self, df, revenue_col='Umsatz', cost_col='Kosten', time_col=None):
    """
    Berechnet wichtige finanzielle Kennzahlen aus einem DataFrame
    
    Args:
        df (DataFrame): DataFrame mit Finanzdaten
        revenue_col (str): Name der Umsatzspalte
        cost_col (str): Name der Kostenspalte
        time_col (str): Name der Zeitspaltespalte (optional)
    
    Returns:
        DataFrame: Erweiterter DataFrame mit berechneten Kennzahlen
    """
    try:
        # Kopie erstellen, um Originaldaten nicht zu verändern
        result = df.copy()
        
        # Deckungsbeitrag (DB1)
        result['DB1'] = result[revenue_col] - result[cost_col]
        
        # Marge (DB in Prozent vom Umsatz)
        result['Marge'] = (result['DB1'] / result[revenue_col] * 100).round(2)
        
        # Cost-to-Revenue-Ratio (Kosten in Prozent vom Umsatz)
        result['Kostenquote'] = (result[cost_col] / result[revenue_col] * 100).round(2)
        
        # Zeitbasierte Berechnungen, wenn Zeitspalte vorhanden
        if time_col and time_col in result.columns:
            # Sicherstellen, dass die Zeitspalte den richtigen Datentyp hat
            if not pd.api.types.is_datetime64_any_dtype(result[time_col]):
                try:
                    result[time_col] = pd.to_datetime(result[time_col])
                except:
                    # Falls Konvertierung nicht möglich, zeitbasierte Berechnungen überspringen
                    return result
            
            # Nach Zeit sortieren
            result = result.sort_values(by=time_col)
            
            # Wachstumsraten (Periode zu Periode)
            result['Umsatzwachstum'] = result[revenue_col].pct_change() * 100
            result['Kostenwachstum'] = result[cost_col].pct_change() * 100
            result['DB_Wachstum'] = result['DB1'].pct_change() * 100
            
            # Gleitende Durchschnitte (3 Perioden)
            result['Umsatz_MA3'] = result[revenue_col].rolling(window=3).mean()
            result['DB1_MA3'] = result['DB1'].rolling(window=3).mean()
            
            # Kumulierte Werte (Year-to-Date, falls Datum ein Jahr enthält)
            if hasattr(result[time_col].dt, 'year'):
                # Gruppierung nach Jahr für YTD-Berechnung
                result['Jahr'] = result[time_col].dt.year
                result['Monat'] = result[time_col].dt.month
                
                # Kumulierte Werte innerhalb des Jahres
                result['Umsatz_YTD'] = result.groupby('Jahr')[revenue_col].cumsum()
                result['Kosten_YTD'] = result.groupby('Jahr')[cost_col].cumsum()
                result['DB1_YTD'] = result['Umsatz_YTD'] - result['Kosten_YTD']
                
                # YTD-Marge
                result['Marge_YTD'] = (result['DB1_YTD'] / result['Umsatz_YTD'] * 100).round(2)
        
        return result
    except Exception as e:
        raise Exception(f"Fehler bei der Kennzahlenberechnung: {str(e)}")
```

### 13.4 Visualisierung der Abweichungsanalyse

Eine wichtige visuelle Darstellung ist die Abweichungsanalyse:

```python
def plot_variance(self, variance_df, key_column, actual_column, plan_column, var_column, var_pct_column=None, title=None):
    """
    Erstellt ein Diagramm zur Visualisierung der Abweichungsanalyse
    
    Args:
        variance_df (DataFrame): DataFrame mit Abweichungsdaten
        key_column (str): Spalte für die X-Achse (z.B. 'Monat')
        actual_column (str): Spalte mit Ist-Werten
        plan_column (str): Spalte mit Plan-Werten
        var_column (str): Spalte mit absoluten Abweichungen
        var_pct_column (str): Spalte mit prozentualen Abweichungen (optional)
        title (str): Diagrammtitel (optional)
    
    Returns:
        Figure: Matplotlib-Figure-Objekt
    """
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    
    try:
        # Figur und Achsen erstellen
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # X-Achsen-Werte
        x = range(len(variance_df))
        width = 0.35
        
        # Balken für Ist- und Plan-Werte
        bars1 = ax1.bar([i - width/2 for i in x], variance_df[actual_column], width, label='Ist', color='#3498db')
        bars2 = ax1.bar([i + width/2 for i in x], variance_df[plan_column], width, label='Plan', color='#2ecc71')
        
        # Y-Achse formatieren
        ax1.set_ylabel('Wert')
        ax1.tick_params(axis='y')
        
        # X-Achse formatieren
        ax1.set_xticks(x)
        ax1.set_xticklabels(variance_df[key_column])
        
        # Legende für Balken
        ax1.legend(loc='upper left')
        
        # Zweite Y-Achse für Abweichung
        ax2 = ax1.twinx()
        
        # Linie für absolute Abweichung
        line = ax2.plot(x, variance_df[var_column], 'r-', marker='o', label='Abweichung', color='#e74c3c')
        
        # Y-Achse für Abweichung formatieren
        ax2.set_ylabel('Abweichung')
        ax2.tick_params(axis='y')
        
        # Wenn prozentuale Abweichung vorhanden ist, auch anzeigen
        if var_pct_column and var_pct_column in variance_df.columns:
            # Prozentuale Abweichungen als Text anzeigen
            for i, val in enumerate(variance_df[var_pct_column]):
                if not pd.isna(val):
                    ax2.annotate(f"{val:.1f}%", 
                               xy=(i, variance_df[var_column].iloc[i]),
                               xytext=(0, 10),
                               textcoords="offset points",
                               ha='center',
                               fontsize=8,
                               bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))
        
        # Nulllinie für Abweichungen
        ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
        
        # Legende für Linie
        ax2.legend(loc='upper right')
        
        # Titel setzen
        if title:
            plt.title(title)
        else:
            plt.title(f"Plan-Ist-Vergleich: {actual_column.split('_')[0]}")
        
        plt.tight_layout()
        
        return fig
    except Exception as e:
        raise Exception(f"Fehler bei der Visualisierung: {str(e)}")
```

## 14. Fortgeschrittene Funktionen und Erweiterungen

### 14.1 Kennwort-Schutz und Benutzerprofile

Für sensible Finanzdaten ist ein Kennwortschutz sinnvoll:

```python
def implement_user_authentication(self):
    """
    Implementiert Benutzerauthentifizierung für die Anwendung
    """
    from app.utils.crypto import encrypt_password, check_password
    
    class LoginDialog(QDialog):
        def __init__(self, parent=None, data_manager=None):
            super().__init__(parent)
            self.data_manager = data_manager
            self.authenticated = False
            self.username = ""
            self.init_ui()
        
        def init_ui(self):
            self.setWindowTitle("Controller Toolbox - Login")
            self.setFixedSize(350, 200)
            
            layout = QVBoxLayout(self)
            
            # Benutzernamelabel und -feld
            username_layout = QHBoxLayout()
            username_label = QLabel("Benutzername:")
            self.username_edit = QLineEdit()
            username_layout.addWidget(username_label)
            username_layout.addWidget(self.username_edit)
            
            # Passwortlabel und -feld
            password_layout = QHBoxLayout()
            password_label = QLabel("Passwort:")
            self.password_edit = QLineEdit()
            self.password_edit.setEchoMode(QLineEdit.Password)
            password_layout.addWidget(password_label)
            password_layout.addWidget(self.password_edit)
            
            # Buttons
            button_layout = QHBoxLayout()
            login_button = QPushButton("Anmelden")
            login_button.clicked.connect(self.check_credentials)
            cancel_button = QPushButton("Abbrechen")
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(login_button)
            button_layout.addWidget(cancel_button)
            
            # Registrierungslink
            register_link = QLabel("<a href='#'>Neuen Benutzer registrieren</a>")
            register_link.setTextFormat(Qt.RichText)
            register_link.linkActivated.connect(self.show_registration)
            
            # Alles zusammenfügen
            layout.addLayout(username_layout)
            layout.addLayout(password_layout)
            layout.addLayout(button_layout)
            layout.addWidget(register_link)
            layout.addStretch()
        
        def check_credentials(self):
            """Überprüft Benutzername und Passwort"""
            username = self.username_edit.text()
            password = self.password_edit.text()
            
            # Benutzerinformationen aus der Datenbank abrufen
            cursor = self.data_manager.conn.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user and check_password(password, user[0]):
                self.authenticated = True
                self.username = username
                self.accept()
            else:
                QMessageBox.warning(self, "Fehler", "Ungültiger Benutzername oder Passwort")
        
        def show_registration(self):
            """Zeigt den Registrierungsdialog an"""
            dialog = RegistrationDialog(self, self.data_manager)
            if dialog.exec() == QDialog.Accepted:
                self.username_edit.setText(dialog.username)
                self.password_edit.setText("")
                QMessageBox.information(self, "Erfolg", "Benutzer erfolgreich registriert. Sie können sich jetzt anmelden.")
    
    # Registrierungsdialog
    class RegistrationDialog(QDialog):
        def __init__(self, parent=None, data_manager=None):
            super().__init__(parent)
            self.data_manager = data_manager
            self.username = ""
            self.init_ui()
        
        def init_ui(self):
            # Implementierung des Registrierungsdialogs
            pass
        
        def register_user(self):
            """Registriert einen neuen Benutzer"""
            # Implementierung der Benutzerregistrierung
            pass
    
    # Anmeldedialog anzeigen und überprüfen
    login_dialog = LoginDialog(self.main_window, self.data_manager)
    if login_dialog.exec() == QDialog.Accepted:
        self.current_user = login_dialog.username
        self.main_window.show_status(f"Angemeldet als: {self.current_user}")
        return True
    else:
        return False
```

### 14.2 Automatisierte Berichte per E-Mail versenden

Eine nützliche Funktion ist das automatische Versenden von Berichten:

```python
def send_report_by_email(self, report_path, recipient, subject=None, body=None):
    """
    Sendet einen Bericht per E-Mail
    
    Args:
        report_path (str): Pfad zur Berichtsdatei
        recipient (str): E-Mail-Adresse des Empfängers
        subject (str): E-Mail-Betreff (optional)
        body (str): E-Mail-Text (optional)
    
    Returns:
        bool: True bei Erfolg, False bei Fehler
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication
    import os
    
    try:
        # E-Mail-Einstellungen aus der Konfiguration laden
        config = self.data_manager.get_config("email")
        
        if not config:
            raise ValueError("E-Mail-Konfiguration nicht gefunden")
        
        # Standardwerte für Betreff und Text
        if subject is None:
            subject = f"Controller Toolbox - Bericht: {os.path.basename(report_path)}"
        
        if body is None:
            body = f"""
            Sehr geehrte(r) Empfänger(in),
            
            im Anhang finden Sie den automatisch generierten Controlling-Bericht.
            
            Mit freundlichen Grüßen
            Controller Toolbox
            """
        
        # E-Mail erstellen
        msg = MIMEMultipart()
        msg['From'] = config.get('sender')
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Text hinzufügen
        msg.attach(MIMEText(body, 'plain'))
        
        # Anhang hinzufügen
        with open(report_path, 'rb') as file:
            attachment = MIMEApplication(file.read(), Name=os.path.basename(report_path))
        
        attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(report_path)}"'
        msg.attach(attachment)
        
        # Verbindung zum Server herstellen und E-Mail senden
        with smtplib.SMTP(config.get('smtp_server'), config.get('smtp_port')) as server:
            if config.get('use_tls', False):
                server.starttls()
            
            server.login(config.get('username'), config.get('password'))
            server.sendmail(config.get('sender'), recipient, msg.as_string())
        
        return True
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")
        return False
```
