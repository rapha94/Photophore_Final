import functools
from math import *
from Views import mainView, labelView, tagView


class View:
    def __init__(self, controller):
        self.controller = controller

        self.mainView = mainView.MainView(self.controller)

        self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(2).widget().clicked.connect(
            self.controller.delete)
        self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(
            1).widget().layout().itemAt(1).widget().clicked.connect(functools.partial(self.controller.addTag,
                                                                    self.mainView.centralWidget().layout().itemAt(
                                                                        0).widget().layout().itemAt(
                                                                        1).widget().layout().itemAt(
                                                                        1).widget().layout().itemAt(
                                                                        0).widget()))
        self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(
            1).widget().layout().itemAt(3).widget().clicked.connect(functools.partial(self.controller.deleteTag,
                                                                    self.mainView.centralWidget().layout().itemAt(
                                                                        0).widget().layout().itemAt(
                                                                        1).widget().layout().itemAt(
                                                                        1).widget().layout().itemAt(
                                                                        2).widget()))
        self.mainView.centralWidget().layout().itemAt(1).widget().layout().itemAt(0).widget().layout().itemAt(
            1).widget().layout().itemAt(1).widget().clicked.connect(functools.partial(self.controller.addMainTag,
                                                                    self.mainView.centralWidget().layout().itemAt(
                                                                        1).widget().layout().itemAt(
                                                                        0).widget().layout().itemAt(
                                                                        1).widget().layout().itemAt(
                                                                        0).widget()))
        self.mainView.centralWidget().layout().itemAt(1).widget().layout().itemAt(0).widget().layout().itemAt(
            1).widget().layout().itemAt(2).widget().clicked.connect(self.controller.switch)

    def update(self, model):
        self.updateImages(model)
        self.updateTags(model)
        self.updateBoard(model)

    def updateBoard(self, model):
        element = model.getElement(model.workingId)
        self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(
            1).widget().layout().itemAt(2).widget().clear()
        self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(
            1).widget().layout().itemAt(2).widget().addItem("Choisir tag")
        for tag in element.tags:
            self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(
                1).widget().layout().itemAt(2).widget().addItem(tag)
        self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(0).widget().setPixmap(
            element.pixmap.scaled(800, 500))
        self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(
            0).widget().setText(
            "Tags : " + ', '.join(element.tags))

    def updateImages(self, model):
        for i in reversed(range(self.mainView.centralWidget().layout().itemAt(1).widget().layout().itemAt(
                1).widget().widget().layout().count())):
            self.mainView.centralWidget().layout().itemAt(1).widget().layout().itemAt(
                1).widget().widget().layout().itemAt(i).widget().setParent(
                None)
        list = sorted(model.elementList,key=lambda x: x.rank, reverse=True)
        if model.workingId != -1 and model.switched:
            list = sorted(model.getDistanceList(),key=lambda x: x.rank, reverse=True)
        for element in list:
            if (set(element.tags) & set(model.filterList)) or not model.filterList:
                img = labelView.Label(element, self)
                img.setPixmap(element.pixmap.scaled(self.mainView.w * 14 / 100, self.mainView.h * 15 / 100))
                img.setFixedHeight(self.mainView.h * 15 / 100)
                img.setFixedWidth(self.mainView.w * 14 / 100)
                img.clicked.connect(functools.partial(self.controller.clicked, element))
                self.mainView.centralWidget().layout().itemAt(1).widget().layout().itemAt(
                    1).widget().widget().layout().addWidget(img, floor(
                    self.mainView.centralWidget().layout().itemAt(1).widget().layout().itemAt(
                        1).widget().widget().layout().count() / 3), self.mainView.centralWidget().layout().itemAt(
                    1).widget().layout().itemAt(1).widget().widget().layout().count() % 3)

    def updateTags(self, model):
        for i in reversed(range(
                self.mainView.centralWidget().layout().itemAt(1).widget().layout().itemAt(0).widget().layout().itemAt(
                    0).widget().widget().layout().count())):
            self.mainView.centralWidget().layout().itemAt(1).widget().layout().itemAt(0).widget().layout().itemAt(
                0).widget().widget().layout().itemAt(i).widget().setParent(
                None)
        self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(
            1).widget().layout().itemAt(0).widget().clear()
        self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(
            1).widget().layout().itemAt(0).widget().addItem("Choisir tag")
        for element in model.tagList:
            lab = tagView.Tag(element.check, element.text)
            lab.layout().itemAt(0).widget().clicked.connect(element.checkBox)
            lab.layout().itemAt(0).widget().clicked.connect(
                functools.partial(self.controller.checkBox, element.check, element.text))
            lab.layout().itemAt(2).widget().clicked.connect(
                functools.partial(self.controller.deleteMainTag, element.id))
            self.mainView.centralWidget().layout().itemAt(1).widget().layout().itemAt(0).widget().layout().itemAt(
                0).widget().widget().layout().addWidget(lab)
            self.mainView.centralWidget().layout().itemAt(0).widget().layout().itemAt(1).widget().layout().itemAt(
                1).widget().layout().itemAt(0).widget().addItem(element.text)