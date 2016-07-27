#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from view.analysis_widget import AnalysisWidget


# noinspection PyPep8Naming
class SpatialAnalysisWidget(AnalysisWidget):

    # noinspection PyArgumentList
    def __init__(self, webView):
        """
        Construct the Spatial Analysis page in the main window. |br|
        A ``LeafletMap.webView`` will be shown on this page.

        :param webView: The ``LeafletMap.webView`` widget.
        """

        super().__init__()

        upperLabel = QtWidgets.QLabel("Spatial Distribution Graph:")
        upperLabel.setBuddy(webView)

        lowerLabel = QtWidgets.QLabel("Spatial Correlation Quotient:")
        lowerLabel.setBuddy(self.tableWidget)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(upperLabel)
        mainLayout.addWidget(webView)
        mainLayout.addWidget(lowerLabel)
        mainLayout.addWidget(self.tableWidget)

        self.setLayout(mainLayout)
