from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

## Documentation for Label class
#
#  Class heritated from QLabel and graphic item of an image
class Label(QLabel):

    dragElement = None
    clicked = pyqtSignal()

    ## Documentation constructor method
    #  @param data data object of the image
    #  @param element view object
    #
    #   Method that initialize TagData object
    def __init__(self, data=None, element=None):
        super().__init__()
        ## @var data
        #  data object of the image
        self.data = data
        ## @var element
        #  view object
        self.element = element
        self.setAcceptDrops(True)

    ## Documentation mouseMoveEvent method
    #
    #   Redefinition of mouseMoveEvent method for drag&drop
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

    ## Documentation mousePressEvent method
    #
    #   Redefinition of mousePressEvent method to be clickable
    def mousePressEvent(self, e):
        super().mousePressEvent(e)

    ## Documentation dragEnterEvent method
    #
    #   Redefinition of dragEnterEvent method for drag&drop
    def dragEnterEvent(self, e):
        e.accept()

    ## Documentation dropEvent method
    #
    #   Redefinition of dropEvent method for drag&drop
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

    ## Documentation mouseReleaseEvent method
    #
    #   Redefinition of mouseReleaseEvent method to be clickable
    def mouseReleaseEvent(self, event):
        self.clicked.emit()