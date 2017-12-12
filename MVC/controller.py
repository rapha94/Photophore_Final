from MVC import view, model
from PyQt5.QtCore import *
import time
from Scripts.VGG16 import vgg16


class Controller:
    def __init__(self):
        self.view = view.View(self)
        self.model = model.Model(self)
        self.view.update(self.model)

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

    def calculDistances(self,paths):
        for path in paths:
            thread = DistanceThread(self.model, path)
            thread.finished.connect(thread.deleteLater)
            thread.start()
            time.sleep(1)

    def switch(self):
        if self.model.workingId != 1:
            self.model.switched = not self.model.switched
            self.view.update(self.model)

    def clicked(self, element):
        self.model.workingId = element.id
        self.view.update(self.model)

    def delete(self):
        if self.model.workingId != -1:
            self.model.deleteData(self.model.workingId)
            self.model.workingId = -1
            self.view.update(self.model)

    def addTag(self, text):
        data = self.model.getElement(self.model.workingId)
        if (self.model.workingId != -1 and text.currentText() != "Choisir tag" and not text.currentText() in data.tags):
            data.tags.append(text.currentText().upper())
            self.view.update(self.model)

    def addMainTag(self, text):
        if (text.toPlainText() != "" and text.toPlainText() != "Ajouter Tag Ici"):
            self.model.newTag(text.toPlainText().upper())
            self.view.update(self.model)

    def deleteTag(self, text):
        data = self.model.getElement(self.model.workingId)
        if (self.model.workingId != -1 and text.currentText() != "Choisir tag"):
            data.tags.remove(text.currentText())
            self.view.update(self.model)

    def deleteMainTag(self, id):
        self.model.deleteTag(id)
        self.view.update(self.model)

    def checkBox(self, check, text):
        if check:
            self.model.filterList.remove(text)
        else:
            self.model.filterList.append(text)
        self.view.update(self.model)


class DistanceThread(QThread):
    def __init__(self, model, path):
        QThread.__init__(self)
        self.model = model
        self.path = path

    def __del__(self):
        self.wait()

    def run(self):
        self.model.calculDistance(self.path)

class VGG16Thread(QThread):
    def __init__(self, model, path):
        QThread.__init__(self)
        self.model = model
        self.path = path

    def __del__(self):
        self.wait()

    def run(self):
        for item in vgg16.getTags(self.path):
            if item[2] > 0.4:
                if item[1].upper() not in self.model.getElement(self.path).tags:
                    self.model.getElement(self.path).tags.append(item[1].upper())
                    if item[1] not in self.model.tagList:
                        self.model.newTag(item[1].upper())
        self.model.save()
        self.model.load()
        self.view.update(self.model)
