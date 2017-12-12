from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Label(QLabel):

    dragElement = None
    clicked = pyqtSignal()

    def __init__(self, data=None, element=None):
        super().__init__()
        self.data = data
        self.element = element
        self.setAcceptDrops(True)

    def mouseMoveEvent(self, e):
        if self.data != None:
            if e.buttons() != Qt.LeftButton:
                return

            Label.dragElement = self.data

            mimeData = QMimeData()
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(e.pos() - self.rect().topLeft())

            dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        if self.data != None:
            if self.dragElement != None:
                save = self.dragElement.rank
                self.dragElement.rank = self.data.rank
                self.data.rank = save
            Label.dragElement = None
            e.setDropAction(Qt.MoveAction)
            e.accept()
            self.element.update(self.element.controller.model)

    def mouseReleaseEvent(self, event):
        self.clicked.emit()