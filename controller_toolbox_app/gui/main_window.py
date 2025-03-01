from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QMessageBox, QStatusBar)
from PyQt6.QtCore import Qt
from gui.tabs.dashboard_tab import DashboardTab
from gui.tabs.import_tab import ImportTab
from gui.tabs.analysis_tab import AnalysisTab
from gui.tabs.visualization_tab import VisualizationTab
from gui.tabs.reporting_tab import ReportingTab


class MainWindow(QMainWindow):
    """Hauptfenster der Anwendung"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controller Toolbox")
        self.setMinimumSize(1200, 800)

        # Statusleiste
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        # Tabs erstellen
        self.init_ui()

    def init_ui(self):
        """Initialisiert die UI-Komponenten"""
        # Zentrale Widget-Struktur
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Tabs für verschiedene Funktionen
        self.dashboard_tab = DashboardTab()
        self.import_tab = ImportTab()
        self.analysis_tab = AnalysisTab()
        self.visualization_tab = VisualizationTab()
        self.reporting_tab = ReportingTab()

        # Tabs hinzufügen
        self.tab_widget.addTab(self.dashboard_tab, "Dashboard")
        self.tab_widget.addTab(self.import_tab, "Datenimport")
        self.tab_widget.addTab(self.analysis_tab, "Analyse")
        self.tab_widget.addTab(self.visualization_tab, "Visualisierung")
        self.tab_widget.addTab(self.reporting_tab, "Reporting")

    def show_status(self, message, timeout=5000):
        """Zeigt eine Statusmeldung an"""
        self.statusBar.showMessage(message, timeout)

    def show_error(self, title, message):
        """Zeigt einen Fehlerdialog an"""
        QMessageBox.critical(self, title, message)

    def show_info(self, title, message):
        """Zeigt einen Informationsdialog an"""
        QMessageBox.information(self, title, message)

    def show_warning(self, title, message):
        """Zeigt einen Warnungsdialog an"""
        QMessageBox.warning(self, title, message)