import os
import unittest
from unittest.mock import patch, mock_open

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton
from my_programms.my_programm_first.general_menu import TabOne


class TestTabOne(unittest.TestCase):
    def setUp(self):
        self.tab_one = TabOne()

    def test_set_image_for_button(self):
        button = QPushButton()
        image_path = './images/start.png'
        self.tab_one.set_image_for_button(button, image_path)
        self.assertIsInstance(button.icon(), QIcon)

    def test_brain(self):
        # Mocking random.choice to always return the same key and word for predictable results
        with patch('random.choice', side_effect=lambda x: list(x)[0]):
            self.tab_one.brain()
        self.assertIsNotNone(self.tab_one.random_key)
        self.assertIsNotNone(self.tab_one.random_wort)
        self.assertEqual(self.tab_one.label_output.text(), self.tab_one.random_wort)

    def test_handle_button_click_correct(self):
        expected_key = list(self.tab_one.prepositions.keys())[0]
        button = QPushButton()
        with patch.object(self.tab_one, 'set_button_style') as mock_set_button_style:
            with patch.object(self.tab_one, 'brain') as mock_brain:
                self.tab_one.handle_button_click(expected_key, button)
        mock_set_button_style.assert_called_once_with(button, 'green')
        self.assertEqual(self.tab_one.richtig, 1)
        self.assertEqual(self.tab_one.grade, 1)
        self.assertEqual(self.tab_one.learned, 1)
        mock_brain.assert_called_once()

    def test_handle_button_click_incorrect(self):
        expected_key = list(self.tab_one.prepositions.keys())[0]
        button = QPushButton()
        with patch.object(self.tab_one, 'set_button_style') as mock_set_button_style:
            with patch.object(self.tab_one, 'set_button_style') as mock_set_button_style_other:
                with patch.object(self.tab_one, 'brain') as mock_brain:
                    self.tab_one.handle_button_click(expected_key + 'incorrect', button)
        mock_set_button_style.assert_called_once_with(button, 'red')
        self.assertEqual(self.tab_one.falsch, 1)
        self.assertEqual(self.tab_one.grade, 0)
        mock_set_button_style_other.assert_called_once_with(self.tab_one.button_akk_dat, 'green')
        mock_brain.assert_called_once()

    def test_button_clicked_start(self):
        with patch.object(self.tab_one, 'brain') as mock_brain:
            self.tab_one.button_clicked_start()
        self.assertFalse(self.tab_one.button_start.isEnabled())
        for button in [self.tab_one.button_restart, self.tab_one.button_akk,
                       self.tab_one.button_akk_dat, self.tab_one.button_dat, self.tab_one.button_stop]:
            self.assertTrue(button.isEnabled())
        mock_brain.assert_called_once()

    def test_button_clicked_stop(self):
        with patch.object(self.tab_one, 'button_clicked_restart') as mock_restart:
            self.tab_one.button_clicked_stop()
        self.assertTrue(self.tab_one.button_start.isEnabled())
        for button in [self.tab_one.button_restart, self.tab_one.button_akk,
                       self.tab_one.button_akk_dat, self.tab_one.button_dat, self.tab_one.button_stop]:
            self.assertFalse(button.isEnabled())
        mock_restart.assert_called_once()

    def test_button_clicked_restart(self):
        with patch.object(self.tab_one, 'brain') as mock_brain:
            self.tab_one.button_clicked_restart()
        self.assertEqual(self.tab_one.richtig, 0)
        self.assertEqual(self.tab_one.falsch, 0)
        self.assertEqual(self.tab_one.learned, 0)
        self.assertEqual(self.tab_one.not_learned, 0)
        mock_brain.assert_called_once()

    def test_load_words_empty_file(self):
        with patch('builtins.open', mock_open(read_data='')) as mock_file:
            with patch('os.makedirs') as mock_makedirs:
                words = self.tab_one.load_words()
        mock_makedirs.assert_called_once_with(os.path.join('./data'), exist_ok=True)
        mock_file.assert_called_once_with(os.path.join('./data', self.tab_one.filename), "r", encoding="utf-8")
        self.assertEqual(words, [])

    def test_load_words_non_empty_file(self):
        file_data = '[{"word": "example", "definition": "an example"}]'
        with patch('builtins.open', mock_open(read_data=file_data)) as mock_file:
            with patch('os.makedirs') as mock_makedirs:
                words = self.tab_one.load_words()
        mock_makedirs.assert_called_once_with(os.path.join('./data'), exist_ok=True)
        mock_file.assert_called_once_with(os.path.join('./data', self.tab_one.filename), "r", encoding="utf-8")
        self.assertEqual(words, [{"word": "example", "definition": "an example"}])

    @patch('os.makedirs')
    def test_load_words_file_not_found(self, mock_makedirs):
        with patch('builtins.open', side_effect=FileNotFoundError):
            with patch('builtins.open', mock_open(read_data='')) as mock_file:
                words = self.tab_one.load_words()
        mock_makedirs.assert_called_once_with(os.path.join('./data'), exist_ok=True)
        mock_file.assert_called_once_with(os.path.join('./data', self.tab_one.filename), "w", encoding="utf-8")
        self.assertEqual(words, [])

    def test_move_key_value_list_value_to_move_not_sufficient(self):
        dict1 = {'key': [['value1', 2], ['value2', 1], ['value3', 0]]}
        dict2 = {}
        key = 'key'
        value_index = 1

        self.tab_one.move_key_value_list(dict1, dict2, key, value_index)

        self.assertEqual(dict1, {'key': [['value1', 2], ['value2', 2], ['value3', 0]]})
        self.assertEqual(dict2, {})
        self.assertEqual(self.tab_one.learned, 0)

    def test_move_key_value_list_value_to_move_sufficient(self):
        dict1 = {'key': [['value1', 2], ['value2', 1], ['value3', 0]]}
        dict2 = {}
        key = 'key'
        value_index = 0

        self.tab_one.move_key_value_list(dict1, dict2, key, value_index)

        self.assertEqual(dict1, {'key': [['value2', 1], ['value3', 0]]})
        self.assertEqual(dict2, {'key': [['value1', 2]]})
        self.assertEqual(self.tab_one.learned, 1)

    def test_move_key_value_list_key_not_in_dict2(self):
        dict1 = {'key': [['value1', 2], ['value2', 1], ['value3', 0]]}
        dict2 = {}
        key = 'new_key'
        value_index = 0

        self.tab_one.move_key_value_list(dict1, dict2, key, value_index)

        self.assertEqual(dict1, {'key': [['value1', 2], ['value2', 1], ['value3', 0]]})
        self.assertEqual(dict2, {'new_key': [['value1', 2]]})
        self.assertEqual(self.tab_one.learned, 1)

    def test_move_key_value_list_empty_values_after_move(self):
        dict1 = {'key': [['value1', 2]]}
        dict2 = {}
        key = 'key'
        value_index = 0

        self.tab_one.move_key_value_list(dict1, dict2, key, value_index)

        self.assertEqual(dict1, {})
        self.assertEqual(dict2, {'key': [['value1', 2]]})
        self.assertEqual(self.tab_one.learned, 1)

    def test_set_button_style(self):
        button = QPushButton()
        color = 'green'
        with patch.object(self.tab_one.timer, 'start') as mock_timer_start:
            with patch('logging.debug') as mock_logging_debug:
                self.tab_one.set_button_style(button, color)
        mock_timer_start.assert_called_once_with(600)
        mock_logging_debug.assert_called_once_with('Set button style.')
        self.assertEqual(button.styleSheet(), f"background-color: {color}")

    def test_reset_button_styles(self):
        buttons = [self.tab_one.button_dat, self.tab_one.button_akk, self.tab_one.button_akk_dat]
        with patch.object(self.tab_one.timer, 'stop') as mock_timer_stop:
            with patch('logging.debug') as mock_logging_debug:
                self.tab_one.reset_button_styles()
        mock_timer_stop.assert_called_once()
        mock_logging_debug.assert_called_once_with('Reset button style.')
        for button in buttons:
            self.assertEqual(button.styleSheet(), "background-color: rgb(255, 255, 255);")


if __name__ == '__main__':
    unittest.main()
