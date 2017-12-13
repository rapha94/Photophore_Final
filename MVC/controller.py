from MVC import view, model
from PyQt5.QtCore import *
import time
from Scripts.VGG16 import vgg16


## Documentation for Controller class
#
#  Controller class of MVC Model
class Controller:
    ## Documentation constructor method
    #
    #   Method that initialize controller object
    def __init__(self):
        ## @var view
        #  view object
        self.view = view.View(self)
        ## @var model
        #  model object
        self.model = model.Model(self)
        self.view.update(self.model)
        ## @var threads
        #  list of threads currently running
        self.threads = []

    ## Documentation addData method
    #  @param paths the list of paths to all the images to add
    #
    #   Method which add new images to the database
    def addData(self, paths):
        for path in paths:
            self.model.newData(path)
        self.view.update(self.model)
        self.model.load()
        for path in paths:
            for item in vgg16.getTags(path):
                if item[2] > 0.4:
                    if item[1].upper() not in self.model.getElement(path).tags:
                        self.model.getElement(path).tags.append(item[1].upper())
                        if item[1] not in self.model.tagList:
                            self.model.newTag(item[1].upper())
            self.model.save()
            self.model.load()
            self.view.update(self.model)

    ## Documentation calculDistances method
    #  @param paths the list of paths to all the images to add
    #
    #   Method which calculate the distances between images and add them to database
    def calculDistances(self,paths):
        for path in paths:
            thread = DistanceThread(self.model, path)
            self.threads.append(thread)
            thread.finished.connect(thread.deleteLater)
            thread.start()
            time.sleep(1)

    ## Documentation addData method
    #  @param paths the list of paths to all the images to add
    #
    #   Method which add new images to the database
    def switch(self):
        if self.model.workingId != 1:
            self.model.switched = not self.model.switched
            self.view.update(self.model)

    ## Documentation clicked method
    #  @param element element clicked
    #
    #   Method that change the image focus by updating the workingId
    def clicked(self, element):
        self.model.workingId = element.id
        self.view.update(self.model)

    ## Documentation delete method
    #
    #   Method that delete the focused image
    def delete(self):
        if self.model.workingId != -1:
            self.model.deleteData(self.model.workingId)
            self.model.workingId = -1
            self.view.update(self.model)

    ## Documentation addTag method
    #  @param text name of tag
    #
    #   Method that add a tag to the focused image
    def addTag(self, text):
        data = self.model.getElement(self.model.workingId)
        if (self.model.workingId != -1 and text.currentText() != "Choisir tag" and not text.currentText() in data.tags):
            data.tags.append(text.currentText().upper())
            self.view.update(self.model)

    ## Documentation clicked method
    #  @param text name of tag
    #
    #   Method that add a tag to the software
    def addMainTag(self, text):
        if (text.toPlainText() != "" and text.toPlainText() != "Ajouter Tag Ici"):
            self.model.newTag(text.toPlainText().upper())
            self.view.update(self.model)

    ## Documentation deleteTag method
    #  @param text name of tag
    #
    #   Method that delete a tag of the focused image
    def deleteTag(self, text):
        data = self.model.getElement(self.model.workingId)
        if (self.model.workingId != -1 and text.currentText() != "Choisir tag"):
            data.tags.remove(text.currentText())
            self.view.update(self.model)

    ## Documentation deleteMainTag method
    #  @param id id of the tag
    #
    #   Method that delete the tag corresponding to the id
    def deleteMainTag(self, id):
        self.model.deleteTag(id)
        self.view.update(self.model)

    ## Documentation clicked method
    #  @param check boolean on checkbox
    #
    #   Method that manage checking of tags
    def checkBox(self, check, text):
        if check:
            self.model.filterList.remove(text)
        else:
            self.model.filterList.append(text)
        self.view.update(self.model)


## Documentation for DistanceThread class
#
#  Thread class which calculates distances between images
class DistanceThread(QThread):
    def __init__(self, model, path):
        QThread.__init__(self)
        self.model = model
        self.path = path

    def __del__(self):
        self.wait()

    ## Documentation calculDistances method
    #
    #   Method which calculate the distances between images and add them to database
    def run(self):
        self.model.calculDistance(self.path)