from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt


class DashboardTab(QWidget):
    """Tab für das Dashboard mit Überblick über wichtige KPIs"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Initialisiert die UI-Komponenten"""
        layout = QVBoxLayout(self)

        # Willkommenstext
        welcome_label = QLabel("Willkommen zur Controller Toolbox")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")

        info_label = QLabel(
            "Diese Anwendung bietet umfassende Funktionen zur Excel-basierten "
            "Datenanalyse, Berichterstellung und Visualisierung für Controller."
        )
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 14px; margin-bottom: 30px;")

        # KPI-Karten
        kpi_group = QGroupBox("Beispiel-KPIs")
        kpi_layout = QGridLayout(kpi_group)

        # Beispiel-KPI-Karten
        kpi_cards = [
            self.create_kpi_card("Umsatz", "1.245.680 €", "+5,2%"),
            self.create_kpi_card("Kosten", "876.432 €", "+3,8%"),
            self.create_kpi_card("Deckungsbeitrag", "369.248 €", "+8,9%"),
            self.create_kpi_card("Marge", "29,6%", "+1,1pp")
        ]

        # KPI-Karten anordnen
        for i, card in enumerate(kpi_cards):
            row = i // 2
            col = i % 2
            kpi_layout.addWidget(card, row, col)

        # Anleitung
        guide_group = QGroupBox("Kurzanleitung")
        guide_layout = QVBoxLayout(guide_group)

        guide_text = QLabel(
            "<ol>"
            "<li><b>Datenimport:</b> Wechseln Sie zum Tab 'Datenimport', um Excel-Dateien zu laden.</li>"
            "<li><b>Analyse:</b> Führen Sie Analysen wie KPI-Berechnung oder Abweichungsanalyse durch.</li>"
            "<li><b>Visualisierung:</b> Erstellen Sie aussagekräftige Diagramme.</li>"
            "<li><b>Reporting:</b> Generieren Sie automatisierte Berichte.</li>"
            "</ol>"
        )
        guide_text.setTextFormat(Qt.TextFormat.RichText)
        guide_text.setWordWrap(True)

        guide_layout.addWidget(guide_text)

        # Alles zusammenfügen
        layout.addWidget(welcome_label)
        layout.addWidget(info_label)
        layout.addWidget(kpi_group)
        layout.addWidget(guide_group)
        layout.addStretch()

    def create_kpi_card(self, title, value, change):
        """Erstellt eine KPI-Karte für das Dashboard"""
        card = QGroupBox(title)
        layout = QVBoxLayout(card)

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        change_label = QLabel(change)
        if change.startswith('+'):
            change_label.setStyleSheet("color: green; font-weight: bold;")
        elif change.startswith('-'):
            change_label.setStyleSheet("color: red; font-weight: bold;")
        change_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(value_label)
        layout.addWidget(change_label)

        return card

    def update_kpis(self, kpi_data):
        """Aktualisiert die KPI-Karten mit aktuellen Daten"""
        # Diese Methode würde in einer vollständigen Implementierung
        # die KPI-Karten mit echten Daten aus der Datenbank aktualisieren
        pass