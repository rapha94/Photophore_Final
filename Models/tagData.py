from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Views import labelView

## Documentation for TagData class
#
#  Class tag parameters
class TagData:
    clicked = pyqtSignal()

    ## Documentation constructor method
    #  @param id id of the image
    #  @param text name of tag
    #  @param check boolean checkbox
    #
    #   Method that initialize TagData object
    def __init__(self, id, text, check):
        super().__init__()
        ## @var id
        #  id of the image
        self.id = id
        ## @var text
        #  name of tag
        self.text = text
        ## @var check
        #  boolean checkbox
        self.check = check

    ## Documentation checkBox method
    #
    #   Method that invert check boolean
    def checkBox(self):
        self.check = not self.check