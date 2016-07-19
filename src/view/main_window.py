#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QDesktopWidget, QTabWidget, QVBoxLayout, \
                            QWidget, QFileDialog, QMessageBox, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from multiDict import MultiDict
from spatialAnalysisWidget import SpatialAnalysisWidget
from temporalAnalysisWidget import TemporalAnalysisWidget
from addSpeciesDialog import AddSpeciesDialog
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

