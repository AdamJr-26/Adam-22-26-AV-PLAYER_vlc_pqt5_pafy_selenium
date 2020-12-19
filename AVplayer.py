from gui.source import MainWindow
from PyQt5.QtWidgets import QApplication,QLabel
from PyQt5.QtCore import QTimer, Qt 
from PyQt5.QtGui import QPixmap
import sys
import time

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # splash screen here
    splash = QPixmap('.\Images\splash.jpg')
    splashLabel = QLabel()
    splashLabel.setPixmap(splash)
    splashLabel.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    splashLabel.show()
    QTimer.singleShot(5000, splashLabel.close)

    time.sleep(5)
    window.resize(1300, 700)
    window.show()
    sys.exit(app.exec_())

