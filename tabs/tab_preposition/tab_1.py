import random
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLCDNumber
from qtpy import uic
import logging
from data.data import *

class TabOne(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./data/untitled.ui', self)
        self.random_key = None
        self.random_wort = None
        self.prepositions = prepositions
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
        self.label_output = self.findChild(QLabel, "label_output")
        self.label_output.setText("Нажмите старт")
        self.lcd_nummer_learned = self.findChild(QLCDNumber, "lcdNumber_learned")
        self.lcd_nummer_learned.display(0)
        self.lcd_nummer_not_learned = self.findChild(QLCDNumber, "lcdNumber_not_learned")
        self.lcd_nummer_not_learned.display(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reset_button_styles)
        self.lcd_nummer_r = self.findChild(QLCDNumber, "lcdNumber_r")
        self.lcd_nummer_r.display(0)
        self.lcd_nummer_f = self.findChild(QLCDNumber, "lcdNumber_f")
        self.lcd_nummer_f.display(0)
        self.richtig = 0
        self.falsch = 0
        self.learned = 0
        self.not_learned = 0
        self.training_in_progress = False
        self.button_images = {
            "pushButton_start": './images/start.png',
            "pushButton_restart": './images/restart.png',
            "pushButton_akk": './images/akk.png',
            "pushButton_dat": './images/dat.png',
            "pushButton_akk_dat": './images/akk_dat.png',
            "pushButton_stop": './images/stop.png'
        }

        # Пройдем по списку кнопок и установим для каждой из них изображение
        for button_name, image_path in self.button_images.items():
            button = self.findChild(QPushButton, button_name)
            if button:
                self.set_image_for_button(button, image_path)

    def set_image_for_button(self, button, image_path):
        pixmap = QPixmap(image_path)
        icon = QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(pixmap.rect().size())

    def brain(self):
        self.random_key = random.choice(list(self.prepositions.keys()))
        self.random_wort = random.choice(self.prepositions[self.random_key])
        self.label_output.setText(self.random_wort)
        self.lcd_nummer_r.display(self.richtig)
        self.lcd_nummer_f.display(self.falsch)
        self.lcd_nummer_learned.display(self.learned)
        self.lcd_nummer_not_learned.display(self.not_learned)

    def handle_button_click(self, expected_key, button):
        if self.random_key == expected_key:
            print('Верно!')
            self.set_button_style(button, 'green')
            self.richtig += 1
            logging.info(f'key={self.random_key}, Correct answer: "{expected_key}"')
        else:
            print('Не верно!')
            self.set_button_style(button, 'red')
            self.falsch += 1
            logging.info(f'key={self.random_key}, Incorrect answer: "{expected_key}"')
            other_button = self.button_dat if expected_key == list(self.prepositions.keys())[0] else self.button_akk_dat
            self.set_button_style(other_button, 'green')
        self.brain()

    def button_clicked_start(self):
        self.brain()
        self.button_start.setEnabled(False)
        for button in [self.button_restart, self.button_akk, self.button_akk_dat, self.button_dat, self.button_stop]:
            button.setEnabled(True)
        logging.info('Training started.')

    def button_clicked_stop(self):
        self.button_start.setEnabled(True)
        """self.button_akk.setEnabled(False)
        self.button_akk_dat.setEnabled(False)
        self.button_dat.setEnabled(False)
        self.button_stop.setEnabled(False)"""
        for button in [self.button_restart, self.button_akk, self.button_akk_dat, self.button_dat, self.button_stop]:
            button.setEnabled(False)
        self.button_clicked_restart()
        self.lcd_nummer_f.display(self.richtig)
        self.lcd_nummer_r.display(self.falsch)
        self.lcd_nummer_not_learned.display(self.not_learned)
        self.lcd_nummer_learned.display(self.learned)
        logging.info('Training stopped.')

    def button_clicked_akk(self):
        self.handle_button_click(list(self.prepositions.keys())[0], self.button_akk)

    def button_clicked_akk_dat(self):
        self.handle_button_click(list(self.prepositions.keys())[1], self.button_akk_dat)

    def button_clicked_dat(self):
        self.handle_button_click(list(self.prepositions.keys())[2], self.button_dat)

    def button_clicked_restart(self):
        self.richtig = 0
        self.falsch = 0
        self.learned = 0
        self.not_learned = 0
        self.brain()

    def set_button_style(self, button, color):
        style = f"background-color: {color}"
        button.setStyleSheet(style)
        self.timer.start(600)

    def reset_button_styles(self):
        for button in [self.button_dat, self.button_akk, self.button_akk_dat]:
            button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.timer.stop()