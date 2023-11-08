import os
import sys
from PyQt5 import uic
from tabs.tab_1 import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tab_one = TabOne()
        self.setCentralWidget(self.tab_one)
        self.tab_one.button_start.clicked.connect(self.tab_one.button_clicked_start)
        self.resize(680, 320)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
