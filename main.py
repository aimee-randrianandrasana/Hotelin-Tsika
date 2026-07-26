import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer

__version__ = "2.0.0"

if "QT_QPA_PLATFORM" not in os.environ:
    os.environ["QT_QPA_PLATFORM"] = "xcb"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from ui.main_window import MainWindow
    win = MainWindow()
    QTimer.singleShot(0, win.showMaximized)
    sys.exit(app.exec())
