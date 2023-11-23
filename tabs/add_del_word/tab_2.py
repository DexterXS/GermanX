from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QListView, QVBoxLayout, QWidget, QPushButton, QMainWindow, QLineEdit
from PyQt5.QtCore import Qt
import json

from qtpy import uic


class DeutschWordManager(QMainWindow):
    def __init__(self, filename="data_deutsch_word"):
        super().__init__()
        uic.loadUi('./data/untitled.ui', self)
        self.art = self.findChild(QLineEdit, "lineEdit_art")
        self.save_word = self.findChild(QPushButton, "pushButton_save_word")
        self.save_word.clicked.connect(self.button_save_word)
        self.delete_word = self.findChild(QPushButton, "pushButton_delete_word")
        self.delete_word.clicked.connect(self.button_delete_word)
        self.filename = filename
        """self.words = self.load_words()

    def load_words(self):
        print(f"Загрузка слов....")
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ошибка")
            return []"""

    def button_save_word(self):
        print(f'Текст из QLineEdit:{self.art.text()}')
        print(f"Сохранение слова... (кнопка)")

    def button_delete_word(self, word):
        self.words = [item for item in self.words if item["word"] != word]
        print(f"Удаление слова... (кнопка)")

    def save_words(self):
        text = self.art.text()
        print(text)
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.words, f)
        print(f"Сохранение слова... (процесс)")


class DeutschWordApp(QWidget):
    def __init__(self):
        super().__init__()
        self.word_manager = DeutschWordManager()
        self.model = QStandardItemModel()
        for item_data in self.word_manager.words:
            item = QStandardItem(
                f"{item_data['word']}: {item_data['artikel']} {item_data['ending']} {item_data['type']}")
            self.model.appendRow(item)
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        layout = QVBoxLayout()
        layout.addWidget(self.list_view)
        self.setLayout(layout)
        self.setAttribute(Qt.WA_QuitOnClose)
        self.list_view.clicked.connect(self.item_clicked)

    def item_clicked(self, index):
        item = self.model.itemFromIndex(index)
        if item:
            print(item.text())

    def closeEvent(self, event):
        self.word_manager.save_words()
        event.accept()
