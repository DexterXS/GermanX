import sys
from PyQt5.QtWidgets import QApplication, QTabWidget

from tabs.add_del_word.tab_2 import DeutschWordManager
from tabs.tab_preposition.tab_1 import *
from settings.log_settings import LogSettings


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tabWidget = QTabWidget()  # Создайте объект QTabWidget
        self.setCentralWidget(self.tabWidget)  # Установите его как центральный виджет
        self.tabWidget.setCurrentIndex(0)
        self.tab_add_del_word = DeutschWordManager()
        self.tab_one = TabOne()
        self.setCentralWidget(self.tab_one)
        self.setFixedSize(450, 640)


if __name__ == "__main__":
    LogSettings()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

