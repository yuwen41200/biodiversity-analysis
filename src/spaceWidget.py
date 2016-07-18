#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QTableWidget, QDesktopWidget, \
                            QTableWidgetItem, QVBoxLayout


# noinspection PyPep8Naming
class SpaceWidget(QWidget):

    # noinspection PyArgumentList
    def __init__(self, webView):
        """
        Construct the Space page in the main window. |br|
        A LeafletMap.webView will be shown on this page.

        :param webView: The LeafletMap.webView widget.
        """

        super().__init__()
        self.view = webView

        upperLabel = QLabel("Spatial Distribution Graph:")
        upperLabel.setBuddy(self.view)

        tableWidget = QTableWidget(5, 3, self)
        tableWidget.setHorizontalHeaderLabels(("Species 1", "Species 2", "Correlation Quotient"))
        tableWidget.setColumnWidth(0, QDesktopWidget().availableGeometry().width() * 0.34)
        tableWidget.setColumnWidth(1, QDesktopWidget().availableGeometry().width() * 0.34)
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.setItem(0, 0, QTableWidgetItem("test 1"))
        tableWidget.setItem(2, 0, QTableWidgetItem("test 2"))
        tableWidget.setSortingEnabled(True)

        lowerLabel = QLabel("Spatial Correlation Quotient:")
        lowerLabel.setBuddy(tableWidget)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(upperLabel)
        mainLayout.addWidget(self.view)
        mainLayout.addWidget(lowerLabel)
        mainLayout.addWidget(tableWidget)

        self.setLayout(mainLayout)
