#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from view.spatial_analysis_widget import SpatialAnalysisWidget
from view.temporal_analysis_widget import TemporalAnalysisWidget


# noinspection PyPep8Naming
class MainWindow(QtWidgets.QMainWindow):

    # noinspection PyArgumentList
    def __init__(self):
        """
        Initialize the main window.
        """

        super().__init__()

        self.action = None
        self.map = None
        self.speciesLayout = QtWidgets.QHBoxLayout()

    # noinspection PyArgumentList
    def setupWidgets(self, mainAction, leafletMap):
        """
        Construct all GUI elements on the main window.

        :param mainAction: MainAction controller.
        :param leafletMap: LeafletMap controller.
        :return: None.
        """

        self.action = mainAction
        self.map = leafletMap

        self.setWindowTitle("Biodiversity Analysis")
        self.resize(QtWidgets.QDesktopWidget().availableGeometry().size())

        menuBar = self.menuBar()
        self.statusBar()

        importDataAction = menuBar.addAction("&Import Data")
        importDataAction.setStatusTip("Click to import data.")
        importDataAction.triggered.connect(self.action.importData)

        addSpeciesAction = menuBar.addAction("&Add Species")
        addSpeciesAction.setStatusTip("Click to add species.")
        addSpeciesAction.triggered.connect(self.action.addSpecies)

        clearDataAction = menuBar.addAction("&Clear Data")
        clearDataAction.setStatusTip("Click to clear data.")
        clearDataAction.triggered.connect(self.action.clearData)

        aboutAction = menuBar.addAction("A&bout")
        aboutAction.setStatusTip("Show information about Biodiversity Analysis.")
        aboutAction.triggered.connect(self.action.about)

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
        Open a file dialog so that the user can choose a file.

        :param title: Dialog title.
        :param extension: Acceptable file extension.
        :return: The name of the file chosen by the user.
        """

        return QtWidgets.QFileDialog.getOpenFileName(self, title, os.getcwd(), extension)[0]

    # noinspection PyPep8Naming, PyArgumentList
    def addSpeciesToLayout(self, dataset, newSpecies, selectedSpecies):
        """
        Add a new species to the map and the species layout.

        :param dataset: Dictionary of {species name: list of coordinates}.
        :param newSpecies: Name of the new species to be added.
        :param selectedSpecies: Dictionary of {selected species name: its Species object}.
        :return: None.
        """

        self.map.add(dataset, newSpecies, selectedSpecies)

        label = QtWidgets.QLabel(newSpecies)
        label.setStyleSheet(
            "background-color: " + selectedSpecies[newSpecies].color + ";"
            "border-radius: 10px;"
            "padding-left: 10px;"
            "padding-right: 10px;"
        )
        label.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        ))

        self.speciesLayout.addWidget(label)

    def removeSpeciesFromLayout(self, indices):
        """
        Remove all species from the map and the species layout.

        :param indices: Indices of the species to be removed.
        :return: None.
        """

        self.map.refresh()

        for i in reversed(indices):
            self.speciesLayout.itemAt(i).widget().setParent(None)
