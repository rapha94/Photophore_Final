import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from MVC import controller

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = controller.Controller()
    sys.exit(app.exec_())
