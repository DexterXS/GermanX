from PyQt5.QtWidgets import QWidget, QLabel


class LabelsSetup(QWidget):
    def __init__(self):
        super(LabelsSetup, self).__init__()
        self.label_output = self.findChild(QLabel, "label_output")
        self.label_output.setText("Click start")