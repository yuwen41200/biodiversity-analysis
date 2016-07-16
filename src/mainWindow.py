#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QMainWindow, QLabel, QTabWidget, QVBoxLayout, QHBoxLayout,\
                            QFileDialog, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from multiDict import MultiDict
from spaceWidget import SpaceWidget
from timeWidget import TimeWidget
from addSpeciesDialog import AddSpeciesDialog
from datasetProcessor import extractDarwinCoreArchive, extractCsv
from species import Species


# noinspection PyPep8Naming
class MainWindow(QMainWindow):

    def __init__(self, leafletMap):
        """
        Initialize the main window, using a LeafletMap.
        It will call MainWindow.setupWidgets().

        :param leafletMap: The LeafletMap object.
        """

        # noinspection PyArgumentList
        super().__init__()
        self.map = leafletMap
        self.dataset = MultiDict()
        self.selectedSpecies = {}
        self.speciesList = QHBoxLayout()
        self.setupWidgets()

    # noinspection PyArgumentList
    def setupWidgets(self):
        """
        Construct all GUI elements.
        It is automatically called by MainWindow.__init__().

        :return: None.
        """

        self.setWindowTitle("Biodiversity Analysis")
        self.setGeometry(300, 200, 1000, 700)

        menuBar = self.menuBar()
        self.statusBar()

        importDataAction = menuBar.addAction("&Import Data")
        importDataAction.setStatusTip("Click to import data.")
        importDataAction.triggered.connect(self.importData)

        addSpeciesAction = menuBar.addAction("&Add Species")
        addSpeciesAction.setStatusTip("Click to add species.")
        addSpeciesAction.triggered.connect(self.addSpecies)

        clearDataAction = menuBar.addAction("&Clear Data")
        clearDataAction.setStatusTip("Click to clear data.")
        clearDataAction.triggered.connect(self.clearData)

        tabWidget = QTabWidget(self)
        tabWidget.addTab(SpaceWidget(self.map.webView), "&Space")
        tabWidget.addTab(TimeWidget(), "&Time")

        self.map.webView.setStatusTip("Drag to change the displayed region.")
        self.map.refreshMap()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addLayout(self.speciesList)


        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(mainLayout)
        self.speciesList.setAlignment(Qt.AlignLeft)

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def importData(self):
        """
        Import data from a Darwin Core Archive (DwC-A).
        Store them in MainWindow.dataset.

        :return: None.
        """

        title, extension = "Select a DwC-A File", "DwC-A File (*.zip)"
        filename = QFileDialog.getOpenFileName(self, title, os.getcwd(), extension)[0]

        if filename:
            # noinspection PyBroadException
            try:
                darwinCoreData = extractDarwinCoreArchive(filename)
                columns = ["decimalLatitude", "decimalLongitude", "scientificName"]
                dataList = extractCsv(darwinCoreData, columns)[1]
            except:
                title = "Invalid DwC-A File"
                content = (
                    "The provided file is either not in DwC-A format or corrupted.\n"
                    "Please select a valid one."
                )
                QMessageBox.critical(self, title, content)
                return

            for r in dataList:
                self.dataset[r[2]] = (r[0], r[1])

            title = "Dataset Successfully Imported"
            content = "{:,d} records have been loaded.".format(len(dataList))
            QMessageBox.information(self, title, content)

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def addSpecies(self):
        """
        Choose a species from the previous dataset.
        Append it to MainWindow.selectedSpecies.
        Then refresh the map.

        :return: None.
        """

        if not self.dataset:
            title, content = "Empty Dataset", "Please import data first."
            QMessageBox.critical(self, title, content)

        elif not Species.available():
            title = "Too Many Species"
            content = "Selecting more than 14 species is not supported."
            QMessageBox.critical(self, title, content)

        else:
            species = [k for k in self.dataset.keys() if k not in self.selectedSpecies]

            dialog = AddSpeciesDialog(species, self.selectedSpecies, self.speciesList)
            dialog.exec_()

            self.map.refreshMap(self.dataset, self.selectedSpecies)

    def clearData(self):
        """
        Clear MainWindow.dataset and MainWindow.selectedSpecies.
        Then refresh the map.

        :return: None.
        """

        self.dataset.clear()
        self.selectedSpecies.clear()

        self.map.refreshMap()
