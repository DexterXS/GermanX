import datetime
import logging
import os


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