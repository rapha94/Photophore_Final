from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Views import labelView


class TagData:
    clicked = pyqtSignal()
    def __init__(self, id, text, check):
        super().__init__()
        self.id = id
        self.text = text
        self.check = check

    def checkBox(self):
        self.check = not self.check