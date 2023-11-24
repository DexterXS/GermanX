import json
import os
import random

from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QListView, QComboBox, QMessageBox
from qtpy import uic
import logging
from data.data import *
from settings.log_settings import LogSettings

LogSettings.logs_settings()


class TabOne(QMainWindow):
    def __init__(self):
        super().__init__()

        # Interface connection in ui format
        uic.loadUi('./data/untitled.ui', self)

        # params tab 1
        self.richtig = 0
        self.falsch = 0
        self.art_right = 0
        self.art_wrong = 0
        self.learned = 0
        self.art_word_grade = 0
        self.art_art_random_selected  = '' # random word for tab 2
        self.full_path = ''
        self.not_learned = self.count_total_words(prepositions)
        self.random_key = None
        self.random_wort = None
        self.prepositions = prepositions
        self.prepositions_learned = prepositions_learned
        self.training_in_progress = False
        self.timer = QTimer(self)
        self.word_data = []
        self.timer.timeout.connect(self.reset_button_styles)

        # params tab 2 and 3
        self.filename = "data_deutsch_word.json"
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

        # Links to images for buttons
        self.button_images = {
            "pushButton_start": './images/start.png',
            "pushButton_restart": './images/restart.png',
            "pushButton_akk": './images/akk.png',
            "pushButton_dat": './images/dat.png',
            "pushButton_akk_dat": './images/akk_dat.png',
            "pushButton_stop": './images/stop.png',
            "pushButton_art_der": './images/der.png',
            "pushButton_art_die": './images/die.png',
            "pushButton_art_das": './images/das.png',
            "pushButton_art_minus": './images/minus.png'

        }
        # buttons tab 2
        self.button_art_start = self.findChild(QPushButton, "pushButton_art_start")
        self.button_art_start.clicked.connect(self.button_clicked_art_start)
        self.button_art_stop = self.findChild(QPushButton, "pushButton_art_stop")
        self.button_art_stop.clicked.connect(self.button_clicked_art_stop)
        self.button_art_minus = self.findChild(QPushButton, "pushButton_art_minus")
        self.button_art_minus.clicked.connect(self.button_clicked_art_minus)
        self.button_art_der = self.findChild(QPushButton, "pushButton_art_der")
        self.button_art_der.clicked.connect(self.button_clicked_art_der)
        self.button_art_die = self.findChild(QPushButton, "pushButton_art_die")
        self.button_art_die.clicked.connect(self.button_clicked_art_die)
        self.button_art_das = self.findChild(QPushButton, "pushButton_art_das")
        self.button_art_das.clicked.connect(self.button_clicked_art_das)

        # labels tab 2
        self.label_art_word = self.findChild(QLabel, "label_art_word")
        self.label_art_word.setText("Click start")

        # buttons tab 3
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

        # lcd nummer tab 2
        self.lcd_nummer_art_right = self.findChild(QLCDNumber, "lcdNumber_art_right")
        self.lcd_nummer_art_right.display(0)
        self.lcd_nummer_art_wrong = self.findChild(QLCDNumber, "lcdNumber_art_wrong")
        self.lcd_nummer_art_wrong.display(0)

        # input data tab 3
        self.art_word = self.findChild(QLineEdit, "lineEdit_art_word")
        self.word = self.findChild(QLineEdit, "lineEdit_word")
        self.end_word = self.findChild(QLineEdit, "lineEdit_end_word")
        self.combo_box = self.findChild(QComboBox, "comboBox_type")
        self.setup_combo_box()

        # Output data tab 3
        self.list_view = self.findChild(QListView, "listView_list_words")
        self.list_view.setModel(self.words_model)

        for button_name, image_path in self.button_images.items():
            button = self.findChild(QPushButton, button_name)
            if button:
                self.set_image_for_button(button, image_path)

    # The method that binds to the picture buttons
    @staticmethod
    def set_image_for_button(button, image_path):
        pixmap = QPixmap(image_path)
        icon = QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(pixmap.rect().size())
        logging.debug(f'set image for button: {button}')

    # Method that generates random words for tab 1 and updates information by numbers
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

    # Method that generates random words for tab 2
    def brain_art(self):
        random_art_word = random.choice(self.word_data)
        logging.debug(f"brain_art: random_art_word(list) => {random_art_word}")
        self.lcd_nummer_art_right.display(self.art_right)
        self.lcd_nummer_art_wrong.display(self.art_wrong)
        self.art_art_random_selected = random_art_word['art']
        logging.debug(f'generated random wort: {self.art_art_random_selected}')
        return self.label_art_word.setText(f"{random_art_word['word']}")


    # A method that counts the correct answers, controls the color of the buttons,
    # counts the score for both correct
    # and incorrect answers
    def handle_button_click(self, expected_key, button):
        category = expected_key
        index_in_category = 0
        grade = prepositions[category][index_in_category][1]
        if self.random_key == expected_key:
            self.set_button_style(button, 'green')
            self.richtig += 1
            grade += 1
            logging.info(f'key={self.random_key}, '
                         f'Correct: "{expected_key}" richtig: {self.richtig} grade: {grade}')
            prepositions[category][index_in_category][1] = grade # Update the score for each word separately + 1
            logging.debug(f"first: {expected_key} == {self.random_key}")
        else:
            logging.debug(f"first: {self.random_key} != {expected_key}")
            self.set_button_style(button, 'red')
            self.falsch += 1
            if grade <= 9:
                grade -= 3
            logging.info(f'key={self.random_key}, '
                         f'Incorrect: "{expected_key}" falsch: {self.falsch} grade: {grade}')
            if self.random_key == list(self.prepositions.keys())[0]:
                logging.debug(f"second: {self.random_key} == {list(self.prepositions.keys())[0]} Красим акк в зеленый")
                other_button = self.button_akk
            elif self.random_key == list(self.prepositions.keys())[1]:
                logging.debug(f"second: {self.random_key} elif {list(self.prepositions.keys())[1]} Красим акк-датив в зеленый")
                other_button = self.button_akk_dat
            else:
                logging.debug(f"third: {self.random_key} != {list(self.prepositions.keys())[2]} Красим датив в зеленый")
                other_button = self.button_dat
            self.set_button_style(other_button, 'green')
            prepositions[category][index_in_category][1] = grade # Update the score for each word separately - 3
        self.move_key_value_list(self.prepositions, self.prepositions_learned, expected_key, 0)
        self.not_learned = self.count_total_words(prepositions)

        self.brain()

    def handle_button_click_for_art(self, expected_key=''):
        if self.art_art_random_selected == expected_key:
            self.art_right += 1
            logging.debug(f"handle_button_click_for_art: {self.art_art_random_selected} = {expected_key}")
        else:
            self.art_wrong += 1
            logging.debug(f"{self.art_art_random_selected} != {expected_key}")
        self.brain_art()

    # Method that enables tab 1 and disables buttons
    def button_clicked_start(self):
        logging.debug(f'Start Click "button_clicked_start"')

        self.button_start.setEnabled(False)
        for button in [self.button_restart, self.button_akk, self.button_akk_dat, self.button_dat, self.button_stop]:
            button.setEnabled(True)
            logging.debug(f'____{button} setEnabled "True"')
        self.button_clicked_restart()

    # A method that enables tab 2 and enables the explore buttons
    def button_clicked_art_start(self):
        logging.debug(f'Start Click "button_clicked_art_start"')
        self.brain_art()
        self.button_art_start.setEnabled(False)
        for button in [self.button_art_minus,
                       self.button_art_der,
                       self.button_art_die,
                       self.button_art_das,
                       self.button_art_stop]:
            button.setEnabled(True)
            logging.debug(f'____{button} setEnabled "True"')

    # The method that disables tab 1 resets all results and disables the buttons
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

    # The method that is called by pressing the button restart tab 1, to reset the results
    def button_clicked_art_stop(self):
        self.button_art_start.setEnabled(True)
        for button in [self.button_art_minus,
                       self.button_art_der,
                       self.button_art_die,
                       self.button_art_das,
                       self.button_art_stop]:
            button.setEnabled(False)

    # The method that is called by pressing the button restart tab 1, to reset the results
    def button_clicked_restart(self):
        self.richtig = 0
        self.falsch = 0
        self.learned = 0
        self.not_learned = self.count_total_words(prepositions)
        self.brain()
        logging.debug('Click button restart.')

    # The method that is called by pressing the button restart tab 2, to reset the results
    def button_clicked_art_minus(self):
        self.handle_button_click_for_art(expected_key='-')
        logging.debug('Click button minus.')

    # The method that is called by pressing the button akk tab 1
    def button_clicked_akk(self):
        self.handle_button_click(list(self.prepositions.keys())[0], self.button_akk)
        logging.debug('Click button Akk.')

    # The method that is called by pressing the button akk and dat (tab 1)
    def button_clicked_akk_dat(self):
        self.handle_button_click(list(self.prepositions.keys())[1], self.button_akk_dat)
        logging.debug('Click button Akk/Dat.')

    # The method that is called by pressing the button dat tab 1
    def button_clicked_dat(self):
        self.handle_button_click(list(self.prepositions.keys())[2], self.button_dat)
        logging.debug('Click button Dat.')

    # The method that is called by pressing the button der tab 2
    def button_clicked_art_der(self):
        self.handle_button_click_for_art(expected_key='Der')
        logging.debug('Click button der.')

    # The method that is called by typing the button die tab 2
    def button_clicked_art_die(self):
        self.handle_button_click_for_art(expected_key='Die')
        logging.debug('Click button die.')

    # The method that is called by pressing the button das tab 2
    def button_clicked_art_das(self):
        self.handle_button_click_for_art(expected_key='Das')
        logging.debug('Click button das.')

    # The method that sets the color of the buttons when clicking (scrolling) tab 1
    def set_button_style(self, button, color):
        style = f"background-color: {color}"
        button.setStyleSheet(style)
        self.timer.start(600)
        logging.debug('Set button style.')

    # A method that resets the button style when the user clicks on the correct one
    # or wrong answer on 1 tab
    def reset_button_styles(self):
        for button in [self.button_dat, self.button_akk, self.button_akk_dat]:
            button.setStyleSheet("background-color: rgb(100, 100, 100);")
            logging.debug(f'____{button} set background-color: rgb(100, 100, 100);')
        self.timer.stop()
        logging.debug('Reset button style.')

    # The method that sets the list in the drop-down menu on Tab 3
    def setup_combo_box(self):
        combo_box_items = ["Nominativ", "Genitiv", "Dativ", "Akkusativ", "Verb", "Adjektiv", "Adverb", "Artikel",
                           "Pronomen", "Präposition", "Konjunktion", "Interjektion "]
        self.combo_box.addItems(combo_box_items)

    # A method that validates all added words for Tabs 2 and 3,
    # in 2 tabs for Word Study, and
    # in 3 tabs to display a list of all added words
    def load_words(self):
        logging.info('Loading words...')
        try:
            os.makedirs(os.path.dirname(self.full_path), exist_ok=True)

            with open(self.full_path, "r", encoding="utf-8") as f:
                if os.stat(self.full_path).st_size == 0:
                    logging.info('The file is empty. We return an empty list.')
                    self.words_model.clear()
                    return []

                self.word_data = json.load(f)
                self.words_model.clear()
                for item in self.word_data:
                    art_text = item.get("art", "")
                    word_text = item.get("word", "")
                    end_text = item.get("end", "")
                    type_text = item.get("type", "")
                    logging.debug(f"{art_text}, {word_text}, {end_text}, {type_text}")
                    new_item = QStandardItem(f"{art_text} {word_text}({end_text})  ({type_text})")
                    self.words_model.appendRow(new_item)
                logging.info('Words loaded.')
                return self.word_data

        except FileNotFoundError:
            logging.info('File not found. Create a new file.')
            with open(self.full_path, "w", encoding="utf-8"):
                pass
            return []

    # Method that is called by pressing the button to process the word before saving (Tab 3)
    def button_save_word(self):
        art_text = str(self.art_word.text()).strip().capitalize()
        word_text = str(self.word.text()).strip()
        end_text = str(self.end_word.text()).strip().replace("-", "")
        type_text = str(self.combo_box.currentText()).strip()
        if word_text == "":
            self.show_message("Error", text="The 'word' field must not be empty.")
            return
        if art_text == "":
            art_text = "-"
        elif len(art_text) > 3:
            self.show_message("Error", text="The article cannot be more than 3 characters.")
            return
        if end_text == "":
            end_text = "-"
        elif len(end_text) > 3:
            self.show_message("Error", text="The ending cannot be more than 3 characters.")
        else:
            end_text = f"-{end_text.lower()}"
        if type_text in ["Nominativ", "Artikel", "Pronomen"]:
            word_text = word_text.capitalize()
        else:
            word_text = word_text.lower()

        if not self.word_already_exists(word_text):
            self.save_words(art_text.lower(), word_text, end_text.lower(), type_text)
            new_item = QStandardItem(f"{art_text.lower()}/{word_text}/{end_text.lower()} ({type_text})")
            logging.info(f"Save word: {new_item}")
            self.words_model.appendRow(new_item)
        else:
            self.show_message("Error", "The word already exists.")
        self.art_word.clear()
        self.word.clear()
        self.end_word.clear()

    # Method to check if a word is in the dictionary (so as not to save twice) (tab 3)
    def word_already_exists(self, word_text):
        return any(item["word"] == word_text for item in self.words)

    # The method that works when the button is pressed and deletes the word
    # that should be in "Word" (3 Tab)
    def button_delete_word(self):
        word_text = self.word.text().strip()
        if word_text == "":
            self.show_message("Error", text="The 'word' field must not be empty.")
            return

        with open(self.full_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated_data = [item for item in data if item["word"].strip() != word_text]

        if len(updated_data) < len(data):
            with open(self.full_path, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=4)
            self.words = updated_data
        else:
            self.show_message("Error", text="Word not found.")
        self.art_word.clear()
        self.word.clear()
        self.end_word.clear()
        self.load_words()

    # Method of the process of saving words to a file
    def save_words(self, art_text, word_text, end_text, type_text):
        self.words.append({"art": art_text, "word": word_text, "end": end_text, "type": type_text})
        with open(self.full_path, "w", encoding="utf-8") as f:
            json.dump(self.words, f, ensure_ascii=False, indent=4)  # Ensure proper formatting

    # Method for removing learned words from the list of unlearned words (1 Tab)
    def move_key_value_list(self, dict1, dict2, key, value_index=1):
        logging.debug('start transfer word...')
        values = dict1[key]
        logging.debug(f'+___Value: {values} dict1[{key}]')
        if values:
            logging.debug(f'+_______Values: {values}')
            if key not in dict2:
                dict2[key] = []
            value_to_move = values[value_index]
            logging.debug(f'+_______Value: key: {key} not in dict2: {dict2}')
            if value_to_move[1] >= 3:
                dict2[key].append(value_to_move)
                values.pop(value_index)
                self.learned += 1
                logging.debug(f'+_______Value: key: {key} not in dict2: {dict2}')
            else:
                value_to_move[1] += 1
            if not values:
                del dict1[key]

    # Static method that counts all words to create a count of unlearned words (1 Tab)
    @staticmethod
    def count_total_words(dictionary):
        total_words = 0
        for key, value in dictionary.items():
            total_words += len(value)
        return total_words

    # Static method that creates pop-up windows with a message
    @staticmethod
    def show_message(title, text=None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon("./images/germany.png"))
        msg.setWindowTitle(title)
        if text is not None:
            msg.setText(text)
        msg.exec_()
