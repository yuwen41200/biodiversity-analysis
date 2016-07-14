#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from multiDict import MultiDict
from addSpeciesDialog import AddSpeciesDialog
from datasetProcessor import extractDarwinCoreArchive, extractCsv


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
        self.selectedSpecies = []
        self.setupWidgets()

    def setupWidgets(self):
        """
        Construct all GUI elements.
        It is automatically called by MainWindow.__init__().

        :return: None.
        """

        self.setWindowTitle("Biodiversity Analysis")
        self.setGeometry(300, 200, 1000, 700)
        self.show()

        self.map.webView.setStatusTip("Drag to change the displayed region.")
        self.setCentralWidget(self.map.webView)
        self.map.refreshMap()

        self.statusBar()
        menuBar = self.menuBar()

        importDataAction = menuBar.addAction("Import Data")
        importDataAction.setStatusTip("Click to import data.")
        importDataAction.triggered.connect(self.importData)

        addSpeciesAction = menuBar.addAction("Add Species")
        addSpeciesAction.setStatusTip("Click to add species.")
        addSpeciesAction.triggered.connect(self.addSpecies)

        clearDataAction = menuBar.addAction("Clear Data")
        clearDataAction.setStatusTip("Click to clear data.")
        clearDataAction.triggered.connect(self.clearData)

    def importData(self):
        """
        Import data from a Darwin Core Archive (DwC-A).
        Store them in MainWindow.dataset.

        :return: None.
        """

        title, extension = "Select a DwC-A File", "DwC-A File (*.zip)"
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        filename = QFileDialog.getOpenFileName(self, title, os.getcwd(), extension)[0]
        extension = os.path.splitext(filename)[1]

        if not filename:
            # User clicked the "cancel" button or closed the dialog
            pass

        elif extension != ".zip":
            title, content = "Invalid File", "Currently only DwC-A files are supported."
            # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
            QMessageBox.critical(self, title, content)

        else:
            darwinCoreData = extractDarwinCoreArchive(filename)
            columns = ["decimalLatitude", "decimalLongitude", "scientificName"]
            dataList = extractCsv(darwinCoreData, columns)[1]
            for r in dataList:
                self.dataset[r[2]] = (r[0], r[1])

            title = "Dataset Successfully Imported"
            content = "{:,d} records have been loaded.".format(len(dataList))
            # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
            QMessageBox.information(self, title, content)

    def addSpecies(self):
        """
        Choose a species from the previous dataset.
        Append it to MainWindow.selectedSpecies.
        Then refresh the map.

        :return: None.
        """

        if not self.dataset:
            title, content = "Empty Dataset", "Please import data first."
            # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
            QMessageBox.critical(self, title, content)

        else:
            dialog = AddSpeciesDialog(self.dataset.keys(), self.selectedSpecies)
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
