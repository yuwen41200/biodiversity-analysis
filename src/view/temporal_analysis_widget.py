#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from view.analysis_widget import AnalysisWidget


# noinspection PyPep8Naming
class TemporalAnalysisWidget(AnalysisWidget):

    # noinspection PyArgumentList
    def __init__(self, mplCanvas):
        """
        Construct the Temporal Analysis page in the main window. |br|
        A ``ScatterPlot.mplCanvas`` will be shown on this page.

        :param mplCanvas: The ``ScatterPlot.mplCanvas`` widget.
        """

        super().__init__()

        upperLabel = QtWidgets.QLabel("Temporal Distribution &Graph:")
        upperLabel.setMargin(1)
        upperLabel.setBuddy(mplCanvas)

        lowerLabel = QtWidgets.QLabel("Temporal Correlation &Quotient:")
        lowerLabel.setMargin(1)
        lowerLabel.setBuddy(self.tableWidget)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(upperLabel)
        mainLayout.addWidget(mplCanvas)
        mainLayout.addWidget(lowerLabel)
        mainLayout.addWidget(self.tableWidget)

        self.setLayout(mainLayout)
