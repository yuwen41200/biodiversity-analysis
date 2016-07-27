#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


# noinspection PyPep8Naming
class AnalysisWidget(QtWidgets.QWidget):

    # noinspection PyArgumentList
    def __init__(self):
        """
        Initialize a table widget ``AnalysisWidget.tableWidget``.
        """

        super().__init__()

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

    def addSpeciesToTable(self, species1, species2, correlation):
        """
        Insert a new row into ``AnalysisWidget.tableWidget``.

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
        Delete all rows from ``AnalysisWidget.tableWidget``.

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
