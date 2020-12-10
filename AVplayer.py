from gui.source import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1300, 700)
    window.show()
    sys.exit(app.exec_())
    