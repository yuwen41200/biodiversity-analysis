#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from OpenGL import GL
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from datasetProcessor import extractDarwinCoreArchive

class MainWindow(QMainWindow):

    def __init__(self, leafletMap):
        super().__init__()

        self.leafletMap = leafletMap

        self.setupUI()


    def setupUI(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&Import Data")
        action = fileMenu.addAction("Import Data")
        action.triggered.connect(self.openNewDataset)

        self.setGeometry(300, 200, 1000, 700)
        self.setWindowTitle("Biodiversity Explorer")
        self.show()

    def openNewDataset(self):

        # assume we only support Darwin Core Archive(.zip) now
        # default path: current working directory
        fileName, _ = QFileDialog.getOpenFileName(self, "Open a dataset", os.getcwd(), "*.zip")
        _, extension = os.path.splitext(fileName)
        if extension == ".zip":
            try:
                darwinCoreArchive = extractDarwinCoreArchive(fileName)
            except:
                # TODO: show a warning dialog
                return
