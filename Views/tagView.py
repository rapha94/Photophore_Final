from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Views import labelView


class Tag(QWidget):
    clicked = pyqtSignal()
    def __init__(self,check,text):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        box = labelView.Label()
        cross = labelView.Label()
        cross.setPixmap(QPixmap('/home/Vendicare/Projects/PyCharm/Photophore/assets/cross.png').scaled(25, 25, Qt.KeepAspectRatio))
        text = QLabel(text)
        layout.addWidget(box)
        layout.addWidget(text)
        layout.addWidget(cross)
        if not check:
            self.layout().itemAt(0).widget().setPixmap(
                QPixmap('/home/Vendicare/Projects/PyCharm/Photophore/assets/unchecked.png').scaled(25, 25,
                                                                                                   Qt.KeepAspectRatio))
        else:
            self.layout().itemAt(0).widget().setPixmap(
                QPixmap('/home/Vendicare/Projects/PyCharm/Photophore/assets/checked.png').scaled(25, 25,                                                                                            Qt.KeepAspectRatio))

    def mouseReleaseEvent(self, event):
        self.clicked.emit()