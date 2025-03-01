import os
import sqlite3
from pathlib import Path
import pandas as pd


class DataManager:
    """Klasse für die Datenhaltung"""

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
        try:
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()

            # Tabelle für Einstellungen
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            ''')

            # Tabelle für registrierte Datensätze
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')

            self.conn.commit()
        except Exception as e:
            print(f"Fehler bei der Datenbank-Initialisierung: {e}")

    def save_setting(self, key, value):
        """Speichert eine Anwendungseinstellung"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
            ''', (key, str(value)))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Fehler beim Speichern der Einstellung: {e}")
            return False

    def get_setting(self, key, default=None):
        """Liest eine Anwendungseinstellung"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
            result = cursor.fetchone()
            return result[0] if result else default
        except Exception as e:
            print(f"Fehler beim Lesen der Einstellung: {e}")
            return default

    def register_dataset(self, name, description, file_path):
        """Registriert einen Datensatz in der Datenbank"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT OR REPLACE INTO datasets (name, description, file_path)
            VALUES (?, ?, ?)
            ''', (name, description, file_path))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Fehler beim Registrieren des Datensatzes: {e}")
            return False

    def get_datasets(self):
        """Gibt alle registrierten Datensätze zurück"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT name, description, file_path FROM datasets ORDER BY created_at DESC')
            return cursor.fetchall()
        except Exception as e:
            print(f"Fehler beim Abrufen der Datensätze: {e}")
            return []

    def save_dataframe(self, df, file_path, sheet_name="Sheet1", index=True):
        """Speichert einen DataFrame in eine Excel-Datei"""
        try:
            # Verzeichnis erstellen, falls es nicht existiert
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

            # DataFrame speichern
            df.to_excel(file_path, sheet_name=sheet_name, index=index)
            return True
        except Exception as e:
            print(f"Fehler beim Speichern des DataFrames: {e}")
            return False

    def load_dataframe(self, file_path, sheet_name=0):
        """Lädt einen DataFrame aus einer Excel-Datei"""
        try:
            return pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            print(f"Fehler beim Laden des DataFrames: {e}")
            return None

    def get_config(self, section, default=None):
        """Liest eine Konfigurationssektion"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT value FROM settings WHERE key LIKE ?', (f"{section}_%",))
            results = cursor.fetchall()

            if not results:
                return default

            config = {}
            for row in results:
                key = row[0].split('_', 1)[1]
                config[key] = row[0]

            return config
        except Exception as e:
            print(f"Fehler beim Lesen der Konfiguration: {e}")
            return default