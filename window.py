#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from OpenGL import GL
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setupUI()


    def setupUI(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Import Data')

        self.setGeometry(300, 200, 1000, 700)
        self.setWindowTitle('Biodiversity Explorer')
        self.show()
