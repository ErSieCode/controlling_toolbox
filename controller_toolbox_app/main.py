import sys
from PyQt6.QtWidgets import QApplication
from controller import ControllerApp

def main():
    """Haupteinstiegspunkt der Anwendung"""
    app = QApplication(sys.argv)
    controller = ControllerApp()
    controller.main_window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())