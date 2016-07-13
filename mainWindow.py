#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from datasetProcessor import extractDarwinCoreArchive, extractCsv


# noinspection PyPep8Naming
class MainWindow(QMainWindow):

    def __init__(self, leafletMap):
        # noinspection PyArgumentList
        super().__init__()
        self.map = leafletMap
        self.dataset = ""
        self.speciesList = []
        self.setupWidgets()

    def setupWidgets(self):
        self.setWindowTitle("Biodiversity Explorer")
        self.setGeometry(300, 200, 1000, 700)
        self.setCentralWidget(self.map.webView)
        self.show()

        menuBar = self.menuBar()
        importDataAction = menuBar.addAction("Import Data")
        addSpeciesAction = menuBar.addAction("Add Species")
        importDataAction.triggered.connect(self.importData)
        addSpeciesAction.triggered.connect(self.addSpecies)

        self.statusBar().showMessage("Ready.")
        self.map.refreshMap()

    def importData(self):
        """
        Import data from a Darwin Core Archive (DwC-A), store them in `MainWindow.dataset`.

        :return: None.
        """

        title, extension = "Select a DwC-A File", "DwC-A Files (*.zip)"
        # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
        filename = QFileDialog.getOpenFileName(self, title, os.getcwd(), extension)[0]
        extension = os.path.splitext(filename)[1]

        if extension != ".zip":
            title, content = "Invalid File", "Currently only DwC-A files are supported."
            # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
            QMessageBox.critical(self, title, content)
            self.statusBar().showMessage("Please retry.")

        else:
            darwinCoreData = extractDarwinCoreArchive(filename)
            columns = ["decimalLatitude", "decimalLongitude", "scientificName"]
            self.dataset = extractCsv(darwinCoreData, columns)[1]
            self.statusBar().showMessage("Dataset successfully imported.")

    def addSpecies(self):
        """
        Choose a species from the previous dataset, append it to `MainWindow.speciesList`.

        :return: None.
        """

        if not self.dataset:
            title, content = "No Data Loaded", "The dataset is empty."
            # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
            QMessageBox.critical(self, title, content)
            self.statusBar().showMessage("Please retry.")

        else:
            frozenset(r[2] for r in self.dataset)
            pass
            # TODO: Finish it!
