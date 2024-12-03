import sys
import traceback

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from ui.qt_application import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Arial", 14)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
