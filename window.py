#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from OpenGL import GL
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from datasetProcessor import extractDarwinCoreArchive


# noinspection PyPep8Naming
class MainWindow(QMainWindow):

    def __init__(self, leafletMap):
        super().__init__()
        self.setupUi()
        self.leafletMap = leafletMap
        self.setWindowTitle("Biodiversity Explorer")
        self.setGeometry(300, 200, 1000, 700)
        self.setCentralWidget(self.leafletMap.webEngineView)
        self.show()

    def setupUi(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&Import Data")
        action = fileMenu.addAction("Import Data")
        action.triggered.connect(self.openNewDataSet)

    def openNewDataSet(self):
        """
        Assume we only support Darwin Core Archive (zip file) now.
        Default path is current working directory.
        """
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Darwin Core Archive (DwC-A)", os.getcwd(), "*.zip")
        _, extension = os.path.splitext(fileName)
        if extension == ".zip":
            try:
                darwinCoreArchiveData = extractDarwinCoreArchive(fileName)
                self.leafletMap.refreshMap(darwinCoreArchiveData)
            except:
                # TODO: show a warning dialog
                return
