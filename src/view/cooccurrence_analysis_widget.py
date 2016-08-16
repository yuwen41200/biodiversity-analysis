#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from view.analysis_widget import AnalysisWidget


# noinspection PyPep8Naming
class CooccurrenceAnalysisWidget(AnalysisWidget):

    # noinspection PyArgumentList, PyUnresolvedReferences
    def __init__(self):
        """
        Construct the Co-occurrence Analysis page in the main window.
        """

        super().__init__()
        self.limit = 20
        self.cooccurrenceCalculation = None

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setSingleStep(1)
        slider.setPageStep(1)
        slider.setRange(1, 10)
        slider.setValue(2)
        slider.setTracking(True)
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        slider.setTickInterval(1)

        pushButton = QtWidgets.QPushButton("&Limit to 20 Rows")
        pushButton.setDefault(True)

        def recalculate():
            """
            Recalculate the co-occurrence correlation quotient table using the new limit.

            :return: None.
            """

            assert(hasattr(self.cooccurrenceCalculation, "halt"))
            self.limit = slider.value() * 10
            self.cooccurrenceCalculation.halt()

        slider.valueChanged.connect(lambda i: pushButton.setText("&Limit to {}0 Rows".format(i)))
        pushButton.clicked.connect(recalculate)

        upperLabel = QtWidgets.QLabel("&Maximal number of rows returned:")
        upperLabel.setMargin(1)
        upperLabel.setBuddy(slider)

        upperLayout = QtWidgets.QHBoxLayout()
        upperLayout.addWidget(slider)
        upperLayout.addWidget(pushButton)

        lowerLabel = QtWidgets.QLabel("Co-occurrence Correlation &Quotient:")
        lowerLabel.setMargin(1)
        lowerLabel.setBuddy(self.tableWidget)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(upperLabel)
        mainLayout.addLayout(upperLayout)
        mainLayout.addWidget(lowerLabel)
        mainLayout.addWidget(self.tableWidget)

        self.setLayout(mainLayout)
