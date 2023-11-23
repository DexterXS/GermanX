import random
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
        self.label_output.setText("Click start")
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

        for button_name, image_path in self.button_images.items():
            button = self.findChild(QPushButton, button_name)
            if button:
                self.set_image_for_button(button, image_path)

    def set_image_for_button(self, button, image_path):
        pixmap = QPixmap(image_path)
        icon = QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(pixmap.rect().size())
        logging.debug(f'set image for button: {button}')

    def brain(self):
        self.random_key = random.choice(list(self.prepositions.keys()))
        logging.debug(f'generated random key: {self.random_key}')
        self.random_wort = random.choice(self.prepositions[self.random_key])
        logging.debug(f'generated random wort: {self.random_wort}')
        self.label_output.setText(self.random_wort)
        self.lcd_nummer_r.display(self.richtig)
        self.lcd_nummer_f.display(self.falsch)
        self.lcd_nummer_learned.display(self.learned)
        self.lcd_nummer_not_learned.display(self.not_learned)

    def handle_button_click(self, expected_key, button):
        if self.random_key == expected_key:
            self.set_button_style(button, 'green')
            self.richtig += 1
            logging.info(f'key={self.random_key}, Correct answer: "{expected_key}" richtig: {self.richtig}')
        else:
            self.set_button_style(button, 'red')
            self.falsch += 1
            logging.info(f'key={self.random_key}, Incorrect answer: "{expected_key}" falsch: {self.falsch}')
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
