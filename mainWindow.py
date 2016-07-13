#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from addSpeciesDialog import AddSpeciesDialog
from datasetProcessor import extractDarwinCoreArchive, extractCsv, filterSpecies


# noinspection PyPep8Naming
class MainWindow(QMainWindow):

    def __init__(self, leafletMap):
        # noinspection PyArgumentList
        super().__init__()
        self.map = leafletMap
        self.dataset = []
        self.species = frozenset()
        self.selectedSpecies = []
        self.setupWidgets()

    def setupWidgets(self):
        self.setWindowTitle("Biodiversity Explorer")
        self.setGeometry(300, 200, 1000, 700)
        self.setCentralWidget(self.map.webView)
        self.show()

        self.map.refreshMap()
        self.statusBar()
        menuBar = self.menuBar()

        importDataAction = menuBar.addAction("Import Data")
        importDataAction.setStatusTip("Click to import data.")
        importDataAction.triggered.connect(self.importData)

        addSpeciesAction = menuBar.addAction("Add Species")
        addSpeciesAction.setStatusTip("Click to add species.")
        addSpeciesAction.triggered.connect(self.addSpecies)

    def importData(self):
        """
        Import data from a Darwin Core Archive (DwC-A), store them in
        `MainWindow.dataset` and `MainWindow.species`.

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
            self.dataset = extractCsv(darwinCoreData, columns)[1]
            self.species = frozenset(r[2] for r in self.dataset)

            title = "Dataset Successfully Imported"
            content = "{:,d} records have been loaded.".format(len(self.dataset))
            # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
            QMessageBox.information(self, title, content)

    def addSpecies(self):
        """
        Choose a species from the previous dataset, append it to
        `MainWindow.selectedSpecies`.

        :return: None.
        """

        if not self.dataset:
            title, content = "Empty Dataset", "Please import data first."
            # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
            QMessageBox.critical(self, title, content)

        else:
            dialog = AddSpeciesDialog(self.species, self.selectedSpecies)
            dialog.exec_()
            speciesData = filterSpecies(self.dataset, self.selectedSpecies)
            self.map.refreshMap(speciesData)
