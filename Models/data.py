from PyQt5.QtGui import *
import os

class Data:
    def __init__(self, id, rank, path ,tags):
        self.id = id
        self.rank = rank
        self.path = path
        self.tags = tags
        self.pixmap = QPixmap(self.path)

    def delete(self):
        os.remove(self.path)
        del self
