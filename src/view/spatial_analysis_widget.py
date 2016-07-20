#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


# noinspection PyPep8Naming
class SpatialAnalysisWidget(QtWidgets.QWidget):

    # noinspection PyArgumentList
    def __init__(self, webView):
        """
        Construct the Spatial Analysis page in the main window. |br|
        A ``LeafletMap.webView`` will be shown on this page.

        :param webView: The ``LeafletMap.webView`` widget.
        """

        super().__init__()
        self.view = webView

        upperLabel = QtWidgets.QLabel("Spatial Distribution Graph:")
        upperLabel.setBuddy(self.view)

        tableWidget = QtWidgets.QTableWidget(5, 3, self)
        tableWidget.setHorizontalHeaderLabels((
            "Species 1", "Species 2", "Correlation Quotient"
        ))
        tableWidget.setColumnWidth(
            0, QtWidgets.QDesktopWidget().availableGeometry().width() * 0.34
        )
        tableWidget.setColumnWidth(
            1, QtWidgets.QDesktopWidget().availableGeometry().width() * 0.34
        )
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("test 1"))
        tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem("test 2"))
        tableWidget.setSortingEnabled(True)

        lowerLabel = QtWidgets.QLabel("Spatial Correlation Quotient:")
        lowerLabel.setBuddy(tableWidget)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(upperLabel)
        mainLayout.addWidget(self.view)
        mainLayout.addWidget(lowerLabel)
        mainLayout.addWidget(tableWidget)

        self.setLayout(mainLayout)
