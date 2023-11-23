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
    def __init__(self):
        self.log_folder = None

    def logs_settings(self):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d')
        self.log_folder = 'logs'

        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        log_filepath = os.path.join(self.log_folder, f'{formatted_datetime}.log')
        logging.basicConfig(filename=log_filepath, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')