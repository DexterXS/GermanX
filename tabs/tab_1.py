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
        self.label_learned = self.findChild(QLabel, "label_learned")
        self.label_not_learned = self.findChild(QLabel, "label_not_learned")
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
        # Загрузка изображения и установка его на кнопку
        pixmap = QPixmap(image_path)
        icon = QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(pixmap.rect().size())

    # Мозг программы который генерирует рандомный ключ и слово и выводит ошибки и верные ответы на экран
    def brain(self):
        self.random_key = random.choice(list(self.prepositions.keys()))
        self.random_wort = random.choice(self.prepositions[self.random_key])
        self.label_output.setText(self.random_wort)
        self.lcd_nummer_r.display(self.richtig)
        self.lcd_nummer_f.display(self.falsch)
        self.label_learned.setText(self.learned)
        self.label_not_learned.setText(self.not_learned)

    # Кнопка Запуска тренировки (пока что кнопки завершения нет)
    def button_clicked_start(self):
        self.brain()
        self.button_start.setEnabled(False)
        self.button_restart.setEnabled(True)
        self.button_akk.setEnabled(True)
        self.button_akk_dat.setEnabled(True)
        self.button_dat.setEnabled(True)
        self.button_stop.setEnabled(True)
        logging.info('Training started.')

    def button_clicked_stop(self):
        self.button_start.setEnabled(True)
        self.button_restart.setEnabled(False)
        self.button_akk.setEnabled(False)
        self.button_akk_dat.setEnabled(False)
        self.button_dat.setEnabled(False)
        self.button_stop.setEnabled(False)
        logging.info('Training started.')
        pass

    # Кнопка обрабатывающая нажатие "Аккузатив"
    def button_clicked_akk(self):
        if self.random_key == list(self.prepositions.keys())[0]:
            print('Верно!')
            self.set_button_style(self.button_akk, 'green')
            self.richtig += 1
            logging.info(f'key={self.random_key}, Correct answer: "{list(self.prepositions.keys())[0]}"')
        else:
            print('Не верно!')
            self.set_button_style(self.button_akk, 'red')
            self.falsch += 1
            logging.info(f'key={self.random_key}, Incorrect answer: "{list(self.prepositions.keys())[0]}"')
            if self.random_key == list(self.prepositions.keys())[2]:
                self.set_button_style(self.button_dat, 'green')
            else:
                self.set_button_style(self.button_akk_dat, 'green')
        self.brain()

    # Кнопка обрабатывающая нажатие "Датив-Акузатив"
    def button_clicked_akk_dat(self):
        if self.random_key == list(self.prepositions.keys())[1]:
            print('Верно!')
            self.set_button_style(self.button_akk_dat, 'green')
            self.richtig += 1
            logging.info(f'key={self.random_key}, Correct answer: "{list(self.prepositions.keys())[1]}"')
        else:
            print('Не верно!')
            self.set_button_style(self.button_akk_dat, 'red')
            self.falsch += 1
            logging.info(f'key={self.random_key}, Incorrect answer: "{list(self.prepositions.keys())[1]}"')
            if self.random_key == list(self.prepositions.keys())[0]:
                self.set_button_style(self.button_akk, 'green')
            else:
                self.set_button_style(self.button_dat, 'green')
        self.brain()

    # Кнопка обрабатывающая нажатие "Датив"
    def button_clicked_dat(self):
        if self.random_key == list(self.prepositions.keys())[2]:
            print('Верно!')
            self.set_button_style(self.button_dat, 'green')
            self.richtig += 1
            logging.info(f'key={self.random_key}, Correct answer: "{list(self.prepositions.keys())[2]}"')
        else:
            print('Не верно!')
            self.set_button_style(self.button_dat, 'red')
            self.falsch += 1
            logging.info(f'key={self.random_key}, Incorrect answer: "{list(self.prepositions.keys())[2]}"')
            if self.random_key == list(self.prepositions.keys())[0]:
                self.set_button_style(self.button_akk, 'green')
            else:
                self.set_button_style(self.button_akk_dat, 'green')

        self.brain()

    def button_clicked_restart(self):
        self.richtig = 0
        self.falsch = 0
        self.brain()

    # Устанавливает стиль кнопок на Красный или зеленый в зависимости от входящих данных на 300 мс
    def set_button_style(self, button, color):
        style = ""
        if color == 'red':
            style = "background-color: red"
        elif color == 'green':
            style = "background-color: green"
        button.setStyleSheet(style)
        self.timer.start(600)

    # Сбрасывает все стили кнопок на основной цвет
    def reset_button_styles(self):
        self.button_dat.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_akk.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_akk_dat.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.timer.stop()


