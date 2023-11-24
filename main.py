import sys
from PyQt5.QtWidgets import QApplication, QTabWidget

from my_programms.my_programm_first.general_menu import *
from settings.log_settings import LogSettings


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.setCurrentIndex(2)
        self.tab_one = TabOne()
        self.setCentralWidget(self.tab_one)
        self.setFixedSize(450, 640)
        self.setWindowIcon(QIcon("./images/germany.png"))
        self.setWindowTitle("Dexter Deutsch v 1.0")


if __name__ == "__main__":
    LogSettings()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

