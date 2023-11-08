import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap

class PhotoViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Photo Viewer')

        self.label = QLabel(self)
        self.label.setGeometry(10, 10, 380, 180)
        self.label.setAlignment(Qt.AlignCenter)   # Выравнивание по центру

        select_button = QPushButton('Выбрать фото', self)
        select_button.setGeometry(10, 200, 120, 30)
        select_button.clicked.connect(self.showDialog)

    def showDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите фото", "", "Images (*.jpg *.png *.jpeg *.bmp *.gif)", options=options)

        if file_name:
            pixmap = QPixmap(file_name)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)  # Масштабирование изображения

def main():
    app = QApplication(sys.argv)
    viewer = PhotoViewer()
    viewer.show()
    sys.exit(app.exec_())

main()