import json
import os
import random

from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QListView, QComboBox, QMessageBox
from qtpy import uic
import logging
from data.data import *




class TabOne(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./data/untitled.ui', self)

        # params tab 1
        self.richtig = 0
        self.falsch = 0
        self.learned = 0
        self.grade = 0
        self.full_path = ''
        self.not_learned = self.count_total_words(prepositions)
        self.random_key = None
        self.random_wort = None
        self.prepositions = prepositions
        self.training_in_progress = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reset_button_styles)

        # params tab 2 and 3
        self.filename = "data_deutsch_word"
        self.full_path = os.path.join('./data', self.filename)
        self.words_model = QStandardItemModel()
        self.words = self.load_words()

        # buttons tab 1
        self.button_start = self.findChild(QPushButton, "pushButton_start")
        self.button_start.clicked.connect(self.button_clicked_start)
        self.button_stop = self.findChild(QPushButton, "pushButton_stop")
        self.button_stop.clicked.connect(self.button_clicked_stop)
        self.button_restart = self.findChild(QPushButton, "pushButton_restart")
        self.button_restart.clicked.connect(self.button_clicked_restart)
        self.button_akk = self.findChild(QPushButton, "pushButton_akk")
        self.button_akk.clicked.connect(self.button_clicked_akk)
        self.button_dat = self.findChild(QPushButton, "pushButton_dat")
        self.button_dat.clicked.connect(self.button_clicked_dat)
        self.button_akk_dat = self.findChild(QPushButton, "pushButton_akk_dat")
        self.button_akk_dat.clicked.connect(self.button_clicked_akk_dat)
        self.button_images = {
            "pushButton_start": './images/start.png',
            "pushButton_restart": './images/restart.png',
            "pushButton_akk": './images/akk.png',
            "pushButton_dat": './images/dat.png',
            "pushButton_akk_dat": './images/akk_dat.png',
            "pushButton_stop": './images/stop.png'
        }
        # buttons tab 2
        self.save_word = self.findChild(QPushButton, "pushButton_save_word")
        self.save_word.clicked.connect(self.button_save_word)
        self.delete_word = self.findChild(QPushButton, "pushButton_delete_word")
        self.delete_word.clicked.connect(self.button_delete_word)

        # labels tab 1
        self.label_output = self.findChild(QLabel, "label_output")
        self.label_output.setText("Click start")

        # lcd nummer tab 1
        self.lcd_nummer_learned = self.findChild(QLCDNumber, "lcdNumber_learned")
        self.lcd_nummer_learned.display(0)
        self.lcd_nummer_not_learned = self.findChild(QLCDNumber, "lcdNumber_not_learned")
        self.lcd_nummer_not_learned.display(0)
        self.lcd_nummer_r = self.findChild(QLCDNumber, "lcdNumber_r")
        self.lcd_nummer_r.display(0)
        self.lcd_nummer_f = self.findChild(QLCDNumber, "lcdNumber_f")
        self.lcd_nummer_f.display(0)

        # input data tab 2
        self.art_word = self.findChild(QLineEdit, "lineEdit_art_word")
        self.word = self.findChild(QLineEdit, "lineEdit_word")
        self.end_word = self.findChild(QLineEdit, "lineEdit_end_word")
        self.combo_box = self.findChild(QComboBox, "comboBox_type")
        self.setup_combo_box()

        # Output data tab 2
        self.list_view = self.findChild(QListView, "listView_list_words")
        self.list_view.setModel(self.words_model)

        # test code 1041
        #self.manually_add_word_to_model("Der", "Tisch", "-", "Nom")

        for button_name, image_path in self.button_images.items():
            button = self.findChild(QPushButton, button_name)
            if button:
                self.set_image_for_button(button, image_path)

    @staticmethod
    def set_image_for_button(button, image_path):
        pixmap = QPixmap(image_path)
        icon = QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(pixmap.rect().size())
        logging.debug(f'set image for button: {button}')

    def brain(self):
        self.random_key = random.choice(list(self.prepositions.keys()))
        logging.debug(f'generated random key: {self.random_key}')
        self.random_wort = random.choice(self.prepositions[self.random_key])[0]
        logging.debug(f'generated random wort: {self.random_wort}')
        self.label_output.setText(self.random_wort)
        self.lcd_nummer_r.display(self.richtig)
        self.lcd_nummer_f.display(self.falsch)
        self.lcd_nummer_learned.display(self.learned)
        self.lcd_nummer_not_learned.display(self.not_learned)
        self.lcd_nummer_learned.display(self.learned)

    def handle_button_click(self, expected_key, button):
        if self.random_key == expected_key:
            self.set_button_style(button, 'green')
            self.richtig += 1
            self.grade += 1
            logging.info(f'key={self.random_key}, '
                         f'Correct: "{expected_key}" richtig: {self.richtig} grade: {self.grade}')
        else:
            self.set_button_style(button, 'red')
            self.falsch += 1
            if self.grade <= 9:
                self.grade -= 3
            logging.info(f'key={self.random_key}, '
                         f'Incorrect: "{expected_key}" falsch: {self.falsch} grade: {self.grade}')
            other_button = self.button_dat if expected_key == list(self.prepositions.keys())[0] else self.button_akk_dat
            self.set_button_style(other_button, 'green')
        self.brain()

    def button_clicked_start(self):
        self.brain()
        self.button_start.setEnabled(False)
        for button in [self.button_restart, self.button_akk, self.button_akk_dat, self.button_dat, self.button_stop]:
            button.setEnabled(True)
            logging.debug(f'{button} setEnabled "True"')

    def button_clicked_stop(self):
        self.button_start.setEnabled(True)
        for button in [self.button_restart, self.button_akk, self.button_akk_dat, self.button_dat, self.button_stop]:
            button.setEnabled(False)
            logging.debug(f'{button} setEnabled "False"')
        self.button_clicked_restart()
        self.lcd_nummer_f.display(self.richtig)
        self.lcd_nummer_r.display(self.falsch)
        self.lcd_nummer_not_learned.display(self.not_learned)
        self.lcd_nummer_learned.display(self.learned)
        self.label_output.setText("Click start")
        logging.info('Training stopped.')

    def button_clicked_akk(self):
        self.handle_button_click(list(self.prepositions.keys())[0], self.button_akk)
        logging.debug('Click button Akk.')

    def button_clicked_akk_dat(self):
        self.handle_button_click(list(self.prepositions.keys())[1], self.button_akk_dat)
        logging.debug('Click button Akk/Dat.')

    def button_clicked_dat(self):
        self.handle_button_click(list(self.prepositions.keys())[2], self.button_dat)
        logging.debug('Click button Dat.')

    def button_clicked_restart(self):
        self.richtig = 0
        self.falsch = 0
        self.learned = 0
        self.not_learned = 0
        self.brain()
        logging.debug('Click button restart.')

    def set_button_style(self, button, color):
        style = f"background-color: {color}"
        button.setStyleSheet(style)
        self.timer.start(600)
        logging.debug('Set button style.')

    def reset_button_styles(self):
        for button in [self.button_dat, self.button_akk, self.button_akk_dat]:
            button.setStyleSheet("background-color: rgb(255, 255, 255);")
            logging.debug(f'{button} set background-color: rgb(255, 255, 255);')
        self.timer.stop()
        logging.debug('Reset button style.')

    def setup_combo_box(self):
        combo_box_items = ["Nom", "Verb", "что-то еще"]
        self.combo_box.addItems(combo_box_items)

    def load_words(self):
        print("Загрузка слов....")
        try:
            os.makedirs(os.path.dirname(self.full_path), exist_ok=True)

            with open(self.full_path, "r", encoding="utf-8") as f:
                if os.stat(self.full_path).st_size == 0:
                    print("Файл пуст. Возвращаем пустой список.")
                    self.words_model.clear()
                    return []

                word_data = json.load(f)
                self.words_model.clear()
                for item in word_data:
                    art_text = item.get("art", "")
                    word_text = item.get("word", "")
                    end_text = item.get("end", "")
                    type_text = item.get("type", "")
                    print(art_text, word_text, end_text, type_text)
                    new_item = QStandardItem(f"{art_text}/{word_text}/{end_text} ({type_text})")
                    self.words_model.appendRow(new_item)

                return word_data
        except FileNotFoundError:
            print("Файл не найден. Создание нового файла.")
            with open(self.full_path, "w", encoding="utf-8"):
                pass
            return []

    def button_save_word(self):
        art_text = self.art_word.text()
        word_text = self.word.text()
        end_text = self.end_word.text()
        type_text = self.combo_box.currentText()
        if word_text.strip() == "":
            self.show_message("Ошибка", text="Поле 'word' не должно быть пустым.")
            return
        if not self.word_already_exists(word_text):
            print(f"Сохранение слова... (кнопка)")
            self.save_words(art_text, word_text, end_text)
            new_item = QStandardItem(f"{art_text}/{word_text}/{end_text} ({type_text})")
            self.words_model.appendRow(new_item)
        else:
            self.show_message("Слово уже существует.")

    def word_already_exists(self, word_text):
        return any(item["word"] == word_text for item in self.words)

    def button_delete_word(self):
        word_text = self.word.text().strip()
        if word_text == "":
            self.show_message("Ошибка", text="Поле 'word' не должно быть пустым.")
            return

        with open(self.full_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated_data = [item for item in data if item["word"].strip() != word_text]

        if len(updated_data) < len(data):
            with open(self.full_path, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=4)
            print(f"Удаление слова... (кнопка)")
        else:
            self.show_message("Ошибка", text="Слово не найдено.")

        self.load_words()

    def save_words(self, art_text, word_text, end_text):
        self.words.append({"art": art_text, "word": word_text, "end": end_text})
        with open(self.full_path, "w", encoding="utf-8") as f:
            json.dump(self.words, f, ensure_ascii=False, indent=4)  # Ensure proper formatting
        print(f"Сохранение слова... (процесс)")


    def move_key_value_list(self, dict1, dict2, key, value_index):
        values = dict1[key]
        if values:
            if key not in dict2:
                dict2[key] = []
            value_to_move = values[value_index]
            if value_to_move[1] >= 3:
                dict2[key].append(value_to_move)
                values.pop(value_index)
                self.learned += 1
            else:
                value_to_move[1] += 1
            if not values:
                del dict1[key]

    @staticmethod
    def count_total_words(dictionary):
        total_words = 0
        for key, value in dictionary.items():
            total_words += len(value)
        return total_words

    @staticmethod
    def show_message(title, text=None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        if text is not None:
            msg.setText(text)
        msg.exec_()




