import datetime
import logging
import os

"""
DEBUG - Низший уровень, используется для отладочной информации.
INFO - Информационные сообщения о ходе выполнения программы.
WARNING - Предупреждения, которые указывают на возможные проблемы, но не критичны.
ERROR - Сообщения об ошибках, которые привели к некритическим сбоям в программе.
CRITICAL - Сообщения о критических ошибках, которые привели к 
"""


class LogSettings:
    def __init__(self, mode="INFO"):
        self.log_folder = None

    @classmethod
    def logs_settings(cls):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d')
        cls.log_folder = 'logs'

        if not os.path.exists(cls.log_folder):
            os.makedirs(cls.log_folder)
        log_filepath = os.path.join(cls.log_folder, f'{formatted_datetime}.log')
        logging.basicConfig(filename=log_filepath, level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')