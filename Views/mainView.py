from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MainView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.w = QApplication.desktop().width()
        self.h = QApplication.desktop().height()
        self.initUI()
        self.setWindowTitle('Main window')
        self.showMaximized()

    def closeEvent(self, QCloseEvent):
        self.controller.model.save()

    def initUI(self):
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        boardWidget = QWidget()
        boardLayout = QVBoxLayout()
        boardWidget.setLayout(boardLayout)
        boardWidget.setFixedWidth(self.w * 40 / 100)
        layout.addWidget(boardWidget)

        focusLabel = QLabel()
        focusLabel.setPixmap(
            QPixmap('/home/Vendicare/Projects/PyCharm/Photophore/assets/blank.png').scaled(self.w * 40 / 100,
                                                                                           self.h * 40 / 100))
        boardLayout.addWidget(focusLabel)

        tagWidget = QWidget()
        tagLayout = QHBoxLayout()
        tagWidget.setLayout(tagLayout)
        boardLayout.addWidget(tagWidget)

        tagsLabel = QLabel()
        tagsLabel.setWordWrap(True)
        tagsLabel.setText("[Tags]")
        tagLayout.addWidget(tagsLabel)

        editTagWidget = QWidget()
        editTagLayout = QVBoxLayout()
        editTagWidget.setLayout(editTagLayout)
        tagLayout.addWidget(editTagWidget)

        addTagCombo = QComboBox()
        addTagCombo.addItem("Choisir tag")
        editTagLayout.addWidget(addTagCombo)

        addTagButton = QPushButton("Ajouter tag")
        editTagLayout.addWidget(addTagButton)

        deleteTagCombo = QComboBox()
        deleteTagCombo.addItem("Choisir tag")
        editTagLayout.addWidget(deleteTagCombo)

        deleteTagButton = QPushButton("Supprimer tag")
        editTagLayout.addWidget(deleteTagButton)

        deleteButton = QPushButton("Supprimer l'image")
        boardLayout.addWidget(deleteButton)

        mainWidget = QWidget()
        mainLayout = QHBoxLayout()
        mainWidget.setLayout(mainLayout)
        layout.addWidget(mainWidget)

        mainTagWidget = QWidget()
        mainTagLayout = QVBoxLayout()
        mainTagWidget.setLayout(mainTagLayout)
        mainTagWidget.setFixedWidth(self.w * 10 / 100)
        mainLayout.addWidget(mainTagWidget)

        listTagWidget = QWidget()
        listTagLayout = QVBoxLayout()
        listTagWidget.setLayout(listTagLayout)
        scrollTagArea = QScrollArea()
        scrollTagArea.setWidgetResizable(True)
        scrollTagArea.setWidget(listTagWidget)
        mainTagLayout.addWidget(scrollTagArea)

        updateTagWidget = QWidget()
        updateTagLayout = QVBoxLayout()
        updateTagWidget.setLayout(updateTagLayout)
        updateTagWidget.setFixedHeight(self.h * 15 / 100)
        mainTagLayout.addWidget(updateTagWidget)

        addMainTagText = QTextEdit()
        addMainTagText.setText("Ajouter Tag Ici")
        addMainTagText.setFixedHeight(self.h * 3 / 100)
        updateTagLayout.addWidget(addMainTagText)

        addMainTagButton = QPushButton("Ajouter tag")
        updateTagLayout.addWidget(addMainTagButton)

        switchButton = QPushButton("Switch")
        updateTagLayout.addWidget(switchButton)

        gridWidget = QWidget()
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(gridWidget)
        mainLayout.addWidget(scrollArea)

        gridLayout = QGridLayout()
        gridLayout.setSpacing(self.w * 1 / 100)
        gridLayout.setVerticalSpacing(self.w * 1 / 100)
        gridWidget.setLayout(gridLayout)

        exitAct = QAction(QIcon('assets/exit.png'), 'Exit', self)
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        uploadAct = QAction(QIcon('assets/upload.png'), 'Upload', self)
        uploadAct.setStatusTip('Upload image')
        uploadAct.triggered.connect(self.openFileNamesDialog)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
        fileMenu.addAction(uploadAct)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)
        toolbar = self.addToolBar('Upload')
        toolbar.addAction(uploadAct)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "Images Files (*.jpg *.png)", options=options)
        if files:
            self.controller.addData(files)
            self.controller.calculDistances(files)
