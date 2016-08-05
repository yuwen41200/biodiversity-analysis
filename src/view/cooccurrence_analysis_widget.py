#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from view.analysis_widget import AnalysisWidget


# noinspection PyPep8Naming
class CooccurrenceAnalysisWidget(AnalysisWidget):

    # noinspection PyArgumentList
    def __init__(self):
        """
        Construct the Co-occurrence Analysis page in the main window.
        """

        super().__init__()

        label = QtWidgets.QLabel("Co-occurrence Quotient:")
        label.setBuddy(self.tableWidget)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(label)
        mainLayout.addWidget(self.tableWidget)

        self.setLayout(mainLayout)
