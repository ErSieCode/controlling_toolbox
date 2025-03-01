import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os


class ControllerToolbox:
    """Hauptklasse für die Controller-Funktionalitäten"""

    def __init__(self):
        self.data = None
        self.report_date = datetime.now().strftime("%Y-%m-%d")

    def load_excel(self, filepath, sheet_name=0, skiprows=None, usecols=None):
        """Lädt Daten aus einer Excel-Datei"""
        try:
            df = pd.read_excel(
                filepath,
                sheet_name=sheet_name,
                skiprows=skiprows,
                usecols=usecols
            )
            return df
        except Exception as e:
            raise Exception(f"Fehler beim Laden der Excel-Datei: {str(e)}")

    def save_to_excel(self, df, filepath, sheet_name="Report", index=True, autoformat=False):
        """Speichert Daten in eine Excel-Datei"""
        try:
            # Verzeichnis erstellen, falls es nicht existiert
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)

            # Daten speichern
            df.to_excel(
                filepath,
                sheet_name=sheet_name,
                index=index
            )

            # Bei Bedarf Autoformat anwenden
            if autoformat:
                # Hier könnte ein erweitertes Formatting mit openpyxl erfolgen
                pass

            return filepath
        except Exception as e:
            raise Exception(f"Fehler beim Speichern der Excel-Datei: {str(e)}")

    def clean_data(self, df):
        """Bereinigt Daten (Entfernt Duplikate, behandelt NaN-Werte)"""
        if df is None:
            raise ValueError("Kein DataFrame übergeben")

        # Kopie erstellen
        result = df.copy()

        # Duplikate entfernen
        result = result.drop_duplicates()

        # NaN-Werte behandeln
        numeric_cols = result.select_dtypes(include=['number']).columns
        result[numeric_cols] = result[numeric_cols].fillna(0)

        # Nicht-numerische Spalten
        non_numeric_cols = result.select_dtypes(exclude=['number']).columns
        result[non_numeric_cols] = result[non_numeric_cols].fillna("")

        return result

    def calculate_kpis(self, df, revenue_col='Umsatz', cost_col='Kosten', time_col=None):
        """Berechnet Finanzkennzahlen"""
        if df is None:
            raise ValueError("Kein DataFrame übergeben")

        # Kopie erstellen
        result = df.copy()

        # Grundlegende KPIs berechnen
        result['DB1'] = result[revenue_col] - result[cost_col]
        result['Marge'] = (result['DB1'] / result[revenue_col] * 100).round(2)
        result['Kostenquote'] = (result[cost_col] / result[revenue_col] * 100).round(2)

        # Zeitbasierte Berechnungen, wenn Zeitspalte vorhanden
        if time_col and time_col in result.columns:
            # Sicherstellen, dass die Zeitspalte den richtigen Datentyp hat
            if not pd.api.types.is_datetime64_any_dtype(result[time_col]):
                try:
                    result[time_col] = pd.to_datetime(result[time_col])
                except:
                    pass

            # Nach Zeit sortieren
            result = result.sort_values(by=time_col)

            # Wachstumsraten berechnen
            result['Umsatzwachstum'] = result[revenue_col].pct_change() * 100
            result['Kostenwachstum'] = result[cost_col].pct_change() * 100
            result['DB_Wachstum'] = result['DB1'].pct_change() * 100

        return result

    def variance_analysis(self, actual_df, plan_df, key_column, value_columns=None):
        """Führt eine Abweichungsanalyse zwischen Ist- und Plandaten durch"""
        if actual_df is None or plan_df is None:
            raise ValueError("Ist- oder Plan-Daten fehlen")

        # Wenn keine Wertspalten angegeben wurden, gemeinsame numerische Spalten verwenden
        if value_columns is None:
            actual_numeric = actual_df.select_dtypes(include=['number']).columns
            plan_numeric = plan_df.select_dtypes(include=['number']).columns
            value_columns = list(set(actual_numeric).intersection(set(plan_numeric)))
            # key_column ausschließen, falls es numerisch ist
            if key_column in value_columns:
                value_columns.remove(key_column)

        # Dataframes auf key_column und value_columns beschränken
        actual_subset = actual_df[[key_column] + value_columns].copy()
        plan_subset = plan_df[[key_column] + value_columns].copy()

        # Suffix für die Spalten
        actual_suffix = "_ist"
        plan_suffix = "_plan"

        # Umbenennen der Wertspalten
        actual_columns = {col: f"{col}{actual_suffix}" for col in value_columns}
        plan_columns = {col: f"{col}{plan_suffix}" for col in value_columns}

        actual_subset = actual_subset.rename(columns=actual_columns)
        plan_subset = plan_subset.rename(columns=plan_columns)

        # Zusammenführen der Daten
        merged = pd.merge(actual_subset, plan_subset, on=key_column, how='outer')

        # Berechnung der Abweichungen
        for col in value_columns:
            actual_col = f"{col}{actual_suffix}"
            plan_col = f"{col}{plan_suffix}"

            # Absolute Abweichung
            merged[f"{col}_var"] = merged[actual_col] - merged[plan_col]

            # Prozentuale Abweichung
            merged[f"{col}_var_pct"] = (merged[f"{col}_var"] / merged[plan_col] * 100).round(2)

        return merged

    def plot_time_series(self, df, x_col='Datum', y_col='Wert', title='Zeitreihenanalyse'):
        """Erstellt ein Zeitreihendiagramm"""
        if df is None:
            raise ValueError("Kein DataFrame übergeben")

        fig, ax = plt.subplots(figsize=(10, 6))

        # Daten plotten
        ax.plot(df[x_col], df[y_col], marker='o', linestyle='-', color='#3498db')

        # Achsenbeschriftungen
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(title)

        # Gitternetzlinien
        ax.grid(True, linestyle='--', alpha=0.7)

        # Datumsformatierung bei Zeitachse
        if pd.api.types.is_datetime64_any_dtype(df[x_col]):
            fig.autofmt_xdate()

        plt.tight_layout()
        return fig

    def plot_variance(self, variance_df, key_column, actual_column, plan_column, var_column, title=None):
        """Erstellt ein Diagramm zur Abweichungsanalyse"""
        if variance_df is None:
            raise ValueError("Kein DataFrame übergeben")

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # X-Achsen-Werte
        x = range(len(variance_df))
        width = 0.35

        # Balken für Ist- und Plan-Werte
        bars1 = ax1.bar([i - width / 2 for i in x], variance_df[actual_column], width, label='Ist', color='#3498db')
        bars2 = ax1.bar([i + width / 2 for i in x], variance_df[plan_column], width, label='Plan', color='#2ecc71')

        # Y-Achse formatieren
        ax1.set_ylabel('Wert')
        ax1.tick_params(axis='y')

        # X-Achse formatieren
        ax1.set_xticks(x)
        ax1.set_xticklabels(variance_df[key_column])

        # Zweite Y-Achse für Abweichung
        ax2 = ax1.twinx()

        # Linie für absolute Abweichung
        line = ax2.plot(x, variance_df[var_column], 'r-', marker='o', label='Abweichung', color='#e74c3c')

        # Y-Achse für Abweichung formatieren
        ax2.set_ylabel('Abweichung')
        ax2.tick_params(axis='y')

        # Nulllinie für Abweichungen
        ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)

        # Legenden
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Titel setzen
        if title:
            plt.title(title)
        else:
            plt.title(f"Plan-Ist-Vergleich: {actual_column.split('_')[0]}")

        plt.tight_layout()
        return fig

    def create_excel_report(self, data_dict, template_path=None, output_path=None):
        """Erstellt einen Excel-Bericht"""
        # Wenn kein Ausgabepfad angegeben, einen erstellen
        if output_path is None:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"Bericht_{now}.xlsx"

        # Excel-Writer mit Pandas erstellen
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Für jeden DataFrame im Dictionary
            for sheet_name, df in data_dict.items():
                # DataFrame ins Excel schreiben
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        return output_path