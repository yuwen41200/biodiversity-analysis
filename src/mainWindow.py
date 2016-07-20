#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QDesktopWidget, QTabWidget, QVBoxLayout, \
                            QWidget, QFileDialog, QMessageBox, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from multiDict import MultiDict
from spatialAnalysisWidget import SpatialAnalysisWidget
from temporalAnalysisWidget import TemporalAnalysisWidget
from addSpeciesDialog import AddSpeciesDialog
from datasetProcessor import extractDarwinCoreArchive, extractCsv
from species import Species


# noinspection PyPep8Naming
class MainWindow(QMainWindow):

    def __init__(self, leafletMap):
        """
        Initialize the main window, using a LeafletMap. |br|
        It will call MainWindow.setupWidgets().

        :param leafletMap: The LeafletMap object.
        """

        # noinspection PyArgumentList
        super().__init__()
        self.map = leafletMap
        self.dataset = MultiDict()
        self.selectedSpecies = {}
        self.speciesLayout = QHBoxLayout()
        self.setupWidgets()

    # noinspection PyArgumentList
    def setupWidgets(self):
        """
        Construct all GUI elements. |br|
        It is automatically called by MainWindow.__init__().

        :return: None.
        """

        self.setWindowTitle("Biodiversity Analysis")
        self.resize(QDesktopWidget().availableGeometry().size())

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

        aboutAction = menuBar.addAction("A&bout")
        aboutAction.setStatusTip("Show information about Biodiversity Analysis.")
        aboutAction.triggered.connect(self.about)

        tabWidget = QTabWidget(self)
        tabWidget.addTab(SpatialAnalysisWidget(self.map.webView), "&Spatial Analysis")
        tabWidget.addTab(TemporalAnalysisWidget(), "&Temporal Analysis")

        self.map.webView.setStatusTip("Drag to change the displayed region.")
        self.map.refresh()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addLayout(self.speciesLayout)

        self.speciesLayout.setAlignment(Qt.AlignLeft)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(mainLayout)

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def importData(self):
        """
        Import data from a Darwin Core Archive (DwC-A). |br|
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
        Choose a species from the previous dataset. |br|
        Append it to MainWindow.selectedSpecies. |br|
        Then refresh the map.

        :return: None.
        """

        if not self.dataset:
            title, content = "Empty Dataset", "Please import data first."
            QMessageBox.critical(self, title, content)

        elif not Species.available():
            title = "Too Many Species"
            content = "Selecting more than " + str(Species.nColor) + " species is not supported."
            QMessageBox.critical(self, title, content)

        else:
            species = [k for k in self.dataset.keys() if k not in self.selectedSpecies]

            def addSpeciesCallback(newSpecies):
                """
                Add the new species to MainWindow.speciesLayout.

                :param newSpecies: Name of the new species.
                :return: None.
                """

                self.selectedSpecies[newSpecies] = Species()
                self.map.addSpecies(self.dataset, newSpecies, self.selectedSpecies)

                label = QLabel(newSpecies)
                label.setStyleSheet(
                    "background-color: " + self.selectedSpecies[newSpecies].color + ";"
                    "color: white;"
                    "border-radius: 10px;"
                    "padding-left: 10px;"
                    "padding-right: 10px;"
                )
                label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
                # noinspection PyArgumentList
                self.speciesLayout.addWidget(label)

            dialog = AddSpeciesDialog(species, addSpeciesCallback)
            dialog.exec_()

    def clearData(self):
        """
        Clear MainWindow.dataset and MainWindow.selectedSpecies. |br|
        Then refresh the map.

        :return: None.
        """

        self.dataset.clear()
        self.removeSpeciesFromLayout()
        self.map.refresh()

    def removeSpeciesFromLayout(self, name=None):
        """
        Remove a species from the species layout. |br|
        If no species is given, it will remove all species.

        :param name: Name of species to be removed.
        :return: None.
        """

        if name:
            index = list(self.selectedSpecies.keys()).index(name)
            del self.selectedSpecies[name]
            indexes = [index]
        else:
            indexes = range(len(self.selectedSpecies))
            self.selectedSpecies.clear()

        for i in reversed(indexes):
            self.speciesLayout.itemAt(i).widget().setParent(None)

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def about(self):
        """
        Show information about this program.

        :return: None.
        """

        title = "About Biodiversity Analysis"
        content = (
            "<h1>Biodiversity Analysis</h1>"
            "<p><b>Biodiversity Data Analysis and Visualization</b><br>"
            "Copyright (C) 2016 Yu-wen Pwu and Yun-chih Chen<br>"
            "<a href='https://github.com/yuwen41200/biodiversity-analysis'>"
            "https://github.com/yuwen41200/biodiversity-analysis</a></p>"
            "<p>This program is free software: you can redistribute it and/or modify "
            "it under the terms of the GNU General Public License as published by "
            "the Free Software Foundation, either version 3 of the License, or "
            "(at your option) any later version.</p>"
            "<p>This program is distributed in the hope that it will be useful, "
            "but WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
            "GNU General Public License for more details.</p>"
            "<p>You should have received a copy of the GNU General Public License "
            "along with this program. If not, see <a href='http://www.gnu.org/licenses/'>"
            "http://www.gnu.org/licenses/</a>.</p>"
            "<p>&nbsp;</p>"
        )
        QMessageBox.about(self, title, content)
