from src.client.main_window import MainWindow
import sys
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = MainWindow()
    app.exec()
