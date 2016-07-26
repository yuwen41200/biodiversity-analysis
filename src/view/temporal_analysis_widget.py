#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


# noinspection PyPep8Naming
class TemporalAnalysisWidget(QtWidgets.QWidget):

    # noinspection PyArgumentList
    def __init__(self, mplCanvas):
        """
        Construct the Temporal Analysis page in the main window. |br|
        A ``ScatterPlot.mplCanvas`` will be shown on this page.

        :param mplCanvas: The ``ScatterPlot.mplCanvas`` widget.
        """

        super().__init__()

        upperLabel = QtWidgets.QLabel("Temporal Distribution Graph:")
        upperLabel.setBuddy(mplCanvas)

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

        lowerLabel = QtWidgets.QLabel("Temporal Correlation Quotient:")
        lowerLabel.setBuddy(self.tableWidget)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(upperLabel)
        mainLayout.addWidget(mplCanvas)
        mainLayout.addWidget(lowerLabel)
        mainLayout.addWidget(self.tableWidget)

        self.setLayout(mainLayout)

    def addSpeciesToTable(self, species1, species2, correlation):
        """
        Insert a new row into ``SpatialAnalysisWidget.tableWidget``.

        :param species1: Value for "Species 1" column.
        :param species2: Value for "Species 2" column.
        :param correlation: Value for "Correlation Quotient" column.
        :return: None.
        """

        rowCount = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(rowCount + 1)

        self.tableWidget.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(species1))
        self.tableWidget.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(species2))
        correlationStr = "{:08.3f}".format(correlation)
        self.tableWidget.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(correlationStr))

    def removeSpeciesFromTable(self):
        """
        Delete all rows from ``SpatialAnalysisWidget.tableWidget``.

        :return: None.
        """

        self.tableWidget.setRowCount(0)

    def enableAutoSort(self):
        """
        Enable automatic sorting by "Correlation Quotient" column in ascending order.

        :return: None.
        """

        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.sortItems(2)

    def disableAutoSort(self):
        """
        When inserting rows, automatic sorting should be disabled.

        :return: None.
        """

        self.tableWidget.setSortingEnabled(False)
