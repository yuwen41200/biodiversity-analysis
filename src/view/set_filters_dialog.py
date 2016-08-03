#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


# noinspection PyPep8Naming
class SetFiltersDialog(QtWidgets.QDialog):

    # noinspection PyArgumentList, PyUnresolvedReferences
    def __init__(self, xCoordinateMinMax, yCoordinateMinMax, timestampMinMax):
        """
        Construct a dialog that allows the user to select a space-time range. |br|
        This range will be used to filter a population.

        :param xCoordinateMinMax: The range of the x-coordinates in the population.
        :param yCoordinateMinMax: The range of the y-coordinates in the population.
        :param timestampMinMax: The range of the timestamps in the population.
        """

        super().__init__()
        self.xCoordinateMinMax = ()
        self.yCoordinateMinMax = ()
        self.timestampMinMax = ()

        self.xMinSpin = QtWidgets.QDoubleSpinBox()
        self.xMinSpin.setDecimals(7)
        self.xMinSpin.setRange(xCoordinateMinMax[0], xCoordinateMinMax[1])
        self.xMinSpin.setValue(xCoordinateMinMax[0])
        self.xMinSpin.setSingleStep(0.01)

        xMinLabel = QtWidgets.QLabel("M&inimal longitude: ")
        xMinLabel.setBuddy(self.xMinSpin)

        self.xMaxSpin = QtWidgets.QDoubleSpinBox()
        self.xMaxSpin.setDecimals(7)
        self.xMaxSpin.setRange(xCoordinateMinMax[0], xCoordinateMinMax[1])
        self.xMaxSpin.setValue(xCoordinateMinMax[1])
        self.xMaxSpin.setSingleStep(0.01)

        xMaxLabel = QtWidgets.QLabel("M&aximal longitude: ")
        xMaxLabel.setBuddy(self.xMaxSpin)

        s = "Legal value: {0:.7f} ~ {1:.7f}".format(xCoordinateMinMax[0], xCoordinateMinMax[1])
        xDiscLabel = QtWidgets.QLabel(s)

        self.xMinSpin.valueChanged.connect(lambda d: self.xMaxSpin.setMinimum(d))
        self.xMaxSpin.valueChanged.connect(lambda d: self.xMinSpin.setMaximum(d))

        xMinLayout = QtWidgets.QHBoxLayout()
        xMinLayout.addWidget(xMinLabel)
        xMinLayout.addWidget(self.xMinSpin)

        xMaxLayout = QtWidgets.QHBoxLayout()
        xMaxLayout.addWidget(xMaxLabel)
        xMaxLayout.addWidget(self.xMaxSpin)

        self.yMinSpin = QtWidgets.QDoubleSpinBox()
        self.yMinSpin.setDecimals(7)
        self.yMinSpin.setRange(yCoordinateMinMax[0], yCoordinateMinMax[1])
        self.yMinSpin.setValue(yCoordinateMinMax[0])
        self.yMinSpin.setSingleStep(0.01)

        yMinLabel = QtWidgets.QLabel("Mi&nimal latitude: ")
        yMinLabel.setBuddy(self.yMinSpin)

        self.yMaxSpin = QtWidgets.QDoubleSpinBox()
        self.yMaxSpin.setDecimals(7)
        self.yMaxSpin.setRange(yCoordinateMinMax[0], yCoordinateMinMax[1])
        self.yMaxSpin.setValue(yCoordinateMinMax[1])
        self.yMaxSpin.setSingleStep(0.01)

        yMaxLabel = QtWidgets.QLabel("Ma&ximal latitude: ")
        yMaxLabel.setBuddy(self.yMaxSpin)

        s = "Legal value: {0:.7f} ~ {1:.7f}".format(yCoordinateMinMax[0], yCoordinateMinMax[1])
        yDiscLabel = QtWidgets.QLabel(s)

        self.yMinSpin.valueChanged.connect(lambda d: self.yMaxSpin.setMinimum(d))
        self.yMaxSpin.valueChanged.connect(lambda d: self.yMinSpin.setMaximum(d))

        yMinLayout = QtWidgets.QHBoxLayout()
        yMinLayout.addWidget(yMinLabel)
        yMinLayout.addWidget(self.yMinSpin)

        yMaxLayout = QtWidgets.QHBoxLayout()
        yMaxLayout.addWidget(yMaxLabel)
        yMaxLayout.addWidget(self.yMaxSpin)

        self.tMinEdit = QtWidgets.QDateTimeEdit()
        self.tMinEdit.setCalendarPopup(True)
        self.tMinEdit.setDateTimeRange(timestampMinMax[0], timestampMinMax[1])
        self.tMinEdit.setDateTime(timestampMinMax[0])
        self.tMinEdit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")

        tMinLabel = QtWidgets.QLabel("&Minimal time: ")
        tMinLabel.setBuddy(self.tMinEdit)

        self.tMaxEdit = QtWidgets.QDateTimeEdit()
        self.tMaxEdit.setCalendarPopup(True)
        self.tMaxEdit.setDateTimeRange(timestampMinMax[0], timestampMinMax[1])
        self.tMaxEdit.setDateTime(timestampMinMax[1])
        self.tMaxEdit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")

        tMaxLabel = QtWidgets.QLabel("Maximal &time: ")
        tMaxLabel.setBuddy(self.tMaxEdit)

        s = ("Legal value: " + timestampMinMax[0].strftime("%Y-%m-%d %H:%M:%S") +
             " ~ " + timestampMinMax[1].strftime("%Y-%m-%d %H:%M:%S") +
             " " + timestampMinMax[0].strftime("%Z%z"))
        tDiscLabel = QtWidgets.QLabel(s)

        self.tMinEdit.dateTimeChanged.connect(lambda dt: self.tMaxEdit.setMinimumDateTime(dt))
        self.tMaxEdit.dateTimeChanged.connect(lambda dt: self.tMinEdit.setMaximumDateTime(dt))

        tMinLayout = QtWidgets.QHBoxLayout()
        tMinLayout.addWidget(tMinLabel)
        tMinLayout.addWidget(self.tMinEdit)

        tMaxLayout = QtWidgets.QHBoxLayout()
        tMaxLayout.addWidget(tMaxLabel)
        tMaxLayout.addWidget(self.tMaxEdit)

        pushButton = QtWidgets.QPushButton("&Filter")
        pushButton.setDefault(True)

        pushButton.clicked.connect(self.setFiltersHandler)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(xMinLayout)
        mainLayout.addLayout(xMaxLayout)
        mainLayout.addWidget(xDiscLabel)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(yMinLayout)
        mainLayout.addLayout(yMaxLayout)
        mainLayout.addWidget(yDiscLabel)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(tMinLayout)
        mainLayout.addLayout(tMaxLayout)
        mainLayout.addWidget(tDiscLabel)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(pushButton)
        mainLayout.setSizeConstraint(QtWidgets.QVBoxLayout.SetFixedSize)

        self.setWindowTitle("Set Filters")
        self.setLayout(mainLayout)
        self.show()

    def setFiltersHandler(self):
        """
        Handler function for the "Filter" button.

        :return: None.
        """

        self.xCoordinateMinMax = (self.xMinSpin.value(), self.xMaxSpin.value())
        self.yCoordinateMinMax = (self.yMinSpin.value(), self.yMaxSpin.value())
        self.timestampMinMax = (self.tMinEdit.dateTime(), self.tMaxEdit.dateTime())
        self.done(0)
