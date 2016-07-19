#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from view.spatial_analysis_widget import SpatialAnalysisWidget
from view.temporal_analysis_widget import TemporalAnalysisWidget
from controller.main_action import importData, addSpecies, clearData, about


# noinspection PyPep8Naming
class MainWindow(QtWidgets.QMainWindow):

    # noinspection PyArgumentList
    def __init__(self, leafletMap):
        """
        Initialize the main window, using a LeafletMap. |br|
        It will call MainWindow.setupWidgets().

        :param leafletMap: The LeafletMap object.
        """

        super().__init__()
        self.map = leafletMap
        self.speciesLayout = QtWidgets.QHBoxLayout()
        self.setupWidgets()

    # noinspection PyArgumentList
    def setupWidgets(self):
        """
        Construct all GUI elements. |br|
        It is automatically called by MainWindow.__init__().

        :return: None.
        """

        self.setWindowTitle("Biodiversity Analysis")
        self.resize(QtWidgets.QDesktopWidget().availableGeometry().size())

        menuBar = self.menuBar()
        self.statusBar()

        importDataAction = menuBar.addAction("&Import Data")
        importDataAction.setStatusTip("Click to import data.")
        importDataAction.triggered.connect(importData)

        addSpeciesAction = menuBar.addAction("&Add Species")
        addSpeciesAction.setStatusTip("Click to add species.")
        addSpeciesAction.triggered.connect(addSpecies)

        clearDataAction = menuBar.addAction("&Clear Data")
        clearDataAction.setStatusTip("Click to clear data.")
        clearDataAction.triggered.connect(clearData)

        aboutAction = menuBar.addAction("A&bout")
        aboutAction.setStatusTip("Show information about Biodiversity Analysis.")
        aboutAction.triggered.connect(about)

        tabWidget = QtWidgets.QTabWidget(self)
        tabWidget.addTab(SpatialAnalysisWidget(self.map.webView), "&Spatial Analysis")
        tabWidget.addTab(TemporalAnalysisWidget(), "&Temporal Analysis")

        self.map.webView.setStatusTip("Drag to change the displayed region.")
        self.map.refresh()

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addLayout(self.speciesLayout)

        self.speciesLayout.setAlignment(Qt.AlignLeft)

        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setLayout(mainLayout)

    def alert(self, title, text, alertType):
        """
        Show an alert window according to the given alert type.

        :param title: Window title.
        :param text: Window text.
        :param alertType: Alert type.
        :return: None.
        """

        funcTable = {
            0: QtWidgets.QMessageBox.information,
            1: QtWidgets.QMessageBox.question,
            2: QtWidgets.QMessageBox.warning,
            3: QtWidgets.QMessageBox.critical,
            4: QtWidgets.QMessageBox.about,
        }

        func = funcTable.get(alertType, QtWidgets.QMessageBox.information)
        func(self, title, text)

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def openFile(self, title, extension):
        """
        Open a file dialog. |br|
        Let the user choose a file to open.

        :param title: Dialog title.
        :param extension: Acceptable file extension.
        :return: The name of the file chosen by the user.
        """

        return QtWidgets.QFileDialog.getOpenFileName(self, title, os.getcwd(), extension)[0]
