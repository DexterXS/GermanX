import unittest
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication
from tabs.tab_1 import TabOne

class TestTabOne(unittest.TestCase):
    def setUp(self):
        app = QApplication([])
        self.window = TabOne()

    def test_brain(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()