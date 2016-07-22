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

        self.tableWidget = QtWidgets.QTableWidget(0, 3, self)
        self.tableWidget.setHorizontalHeaderLabels((
            "Species 1", "Species 2", "Correlation Quotient"
        ))
        self.tableWidget.setColumnWidth(
            0, QtWidgets.QDesktopWidget().availableGeometry().width() * 0.34
        )
        self.tableWidget.setColumnWidth(
            1, QtWidgets.QDesktopWidget().availableGeometry().width() * 0.34
        )
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget.setSortingEnabled(True)

        lowerLabel = QtWidgets.QLabel("Spatial Correlation Quotient:")
        lowerLabel.setBuddy(self.tableWidget)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(upperLabel)
        mainLayout.addWidget(self.view)
        mainLayout.addWidget(lowerLabel)
        mainLayout.addWidget(self.tableWidget)

        self.setLayout(mainLayout)

    def addSpeciesToTable(self, species1, species2, correlation):
        """
        Insert a new row to ``SpatialAnalysisWidget.tableWidget``.

        :param species1: "Species 1" column.
        :param species2: "Species 2" column.
        :param correlation: "Correlation Quotient" column.
        :return: None.
        """

        rowCount = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rowCount + 1)

        self.tableWidget.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(species1))
        self.tableWidget.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(species2))
        self.tableWidget.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(str(correlation)))
