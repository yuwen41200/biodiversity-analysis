#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from view.clickable_label import ClickableLabel
from lib.taxonomy_query import TaxonomyQuery


# noinspection PyPep8Naming
class MainWindow(QtWidgets.QMainWindow):

    # noinspection PyArgumentList
    def __init__(self):
        """
        Initialize the main window.
        """

        super().__init__()
        self.speciesLayout = QtWidgets.QHBoxLayout()
        self.action = None

    # noinspection PyArgumentList
    def setupWidgets(self, spatialAnalysisWidget, temporalAnalysisWidget, mainAction):
        """
        Construct all GUI elements on the main window.

        :param spatialAnalysisWidget: SpatialAnalysisWidget view.
        :param temporalAnalysisWidget: TemporalAnalysisWidget view.
        :param mainAction: MainAction controller.
        :return: None.
        """

        self.action = mainAction

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
        tabWidget.addTab(spatialAnalysisWidget, "&Spatial Analysis")
        tabWidget.addTab(temporalAnalysisWidget, "&Temporal Analysis")

        self.speciesLayout.setAlignment(Qt.AlignLeft)

        speciesWidget = QtWidgets.QWidget()
        speciesWidget.setLayout(self.speciesLayout)

        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidget(speciesWidget)
        scrollArea.setWidgetResizable(True)
        scrollArea.setMaximumHeight(55)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        mainLayout.addWidget(scrollArea)

        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setLayout(mainLayout)

    def alert(self, title, text, alertType=0):
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
    def openFile(self, title, extension=""):
        """
        Open a file dialog so that the user can choose a file.

        :param title: Dialog title.
        :param extension: Acceptable file extension.
        :return: The name of the file chosen by the user.
        """

        return QtWidgets.QFileDialog.getOpenFileName(self, title, os.getcwd(), extension)[0]

    # noinspection PyArgumentList
    def addSpeciesToLayout(self, newSpecies, newColor):
        """
        Add a new species to the species layout.

        :param newSpecies: Name of the new species to be added.
        :param newColor: Color of the new species to be added.
        :return: None.
        """

        label = ClickableLabel(newSpecies)
        label.setStyleSheet(
            "background-color: " + newColor + ";"
            "color: white;"
            "border-radius: 10px;"
            "padding-left: 10px;"
            "padding-right: 10px;"
        )
        label.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        ))
        label.labelClicked.connect(self.action.removeSpecies)

        def addTaxonomyToolTip(taxonomy, tLabel):
            """
            Add a taxonomy tool tip to the label of the new species.

            :param taxonomy: The scientific classification of the new species.
            :param tLabel: The label of the new species.
            :return: None.
            """

            taxonomyKeys = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]
            toolTip = "<br/>".join(
                ["<strong>" + key.title() + "</strong>: " + taxonomy[key] for key in taxonomyKeys]
            )
            tLabel.setToolTip(toolTip)

        TaxonomyQuery(newSpecies, addTaxonomyToolTip, [label])

        self.speciesLayout.addWidget(label)

    def removeSpeciesFromLayout(self, indices):
        """
        Remove the specified species from the species layout.

        :param indices: Indices of the old species to be removed.
        :return: None.
        """

        for i in reversed(indices):
            self.speciesLayout.itemAt(i).widget().setParent(None)
