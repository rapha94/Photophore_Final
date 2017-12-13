from PyQt5.QtGui import *


## Documentation for Data class
#
#  Class containing images and parameters
class Data:
    ## Documentation constructor method
    #  @param id id of the image
    #  @param rank integer defining user appreciation of the image
    #  @param path path of the image
    #  @param tags tag list of the image
    #
    #   Method that initialize Data object
    def __init__(self, id, rank, path, tags):
        ## @var id
        #  id of the object
        self.id = id
        ## @var rank
        #  integer defining user appreciation of the image
        self.rank = rank
        ## @var path
        #  path oh the image
        self.path = path
        ## @var tags
        #  tag list of the object
        self.tags = tags
        ## @var pixmap
        #  pixmap of the image
        self.pixmap = QPixmap(self.path)
