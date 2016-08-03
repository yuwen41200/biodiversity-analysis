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

        xMinSpin = QtWidgets.QDoubleSpinBox()
        xMinSpin.setDecimals(7)
        xMinSpin.setRange(xCoordinateMinMax[0], xCoordinateMinMax[1])
        xMinSpin.setValue(xCoordinateMinMax[0])
        xMinSpin.setSingleStep(0.01)

        xMinLabel = QtWidgets.QLabel("M&inimal longitude: ")
        xMinLabel.setBuddy(xMinSpin)

        xMaxSpin = QtWidgets.QDoubleSpinBox()
        xMaxSpin.setDecimals(7)
        xMaxSpin.setRange(xCoordinateMinMax[0], xCoordinateMinMax[1])
        xMaxSpin.setValue(xCoordinateMinMax[1])
        xMaxSpin.setSingleStep(0.01)

        xMaxLabel = QtWidgets.QLabel("M&aximal longitude: ")
        xMaxLabel.setBuddy(xMaxSpin)

        s = "Legal value: {0:.7f} ~ {1:.7f}".format(xCoordinateMinMax[0], xCoordinateMinMax[1])
        xDiscLabel = QtWidgets.QLabel(s)

        xMinSpin.valueChanged.connect(lambda d: xMaxSpin.setMinimum(d))
        xMaxSpin.valueChanged.connect(lambda d: xMinSpin.setMaximum(d))

        xMinLayout = QtWidgets.QHBoxLayout()
        xMinLayout.addWidget(xMinLabel)
        xMinLayout.addWidget(xMinSpin)

        xMaxLayout = QtWidgets.QHBoxLayout()
        xMaxLayout.addWidget(xMaxLabel)
        xMaxLayout.addWidget(xMaxSpin)

        yMinSpin = QtWidgets.QDoubleSpinBox()
        yMinSpin.setDecimals(7)
        yMinSpin.setRange(yCoordinateMinMax[0], yCoordinateMinMax[1])
        yMinSpin.setValue(yCoordinateMinMax[0])
        yMinSpin.setSingleStep(0.01)

        yMinLabel = QtWidgets.QLabel("Mi&nimal latitude: ")
        yMinLabel.setBuddy(yMinSpin)

        yMaxSpin = QtWidgets.QDoubleSpinBox()
        yMaxSpin.setDecimals(7)
        yMaxSpin.setRange(yCoordinateMinMax[0], yCoordinateMinMax[1])
        yMaxSpin.setValue(yCoordinateMinMax[1])
        yMaxSpin.setSingleStep(0.01)

        yMaxLabel = QtWidgets.QLabel("Ma&ximal latitude: ")
        yMaxLabel.setBuddy(yMaxSpin)

        s = "Legal value: {0:.7f} ~ {1:.7f}".format(yCoordinateMinMax[0], yCoordinateMinMax[1])
        yDiscLabel = QtWidgets.QLabel(s)

        yMinSpin.valueChanged.connect(lambda d: yMaxSpin.setMinimum(d))
        yMaxSpin.valueChanged.connect(lambda d: yMinSpin.setMaximum(d))

        yMinLayout = QtWidgets.QHBoxLayout()
        yMinLayout.addWidget(yMinLabel)
        yMinLayout.addWidget(yMinSpin)

        yMaxLayout = QtWidgets.QHBoxLayout()
        yMaxLayout.addWidget(yMaxLabel)
        yMaxLayout.addWidget(yMaxSpin)

        tMinEdit = QtWidgets.QDateTimeEdit()
        tMinEdit.setCalendarPopup(True)
        tMinEdit.setDateTimeRange(timestampMinMax[0], timestampMinMax[1])
        tMinEdit.setDateTime(timestampMinMax[0])
        tMinEdit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")

        tMinLabel = QtWidgets.QLabel("&Minimal time: ")
        tMinLabel.setBuddy(tMinEdit)

        tMaxEdit = QtWidgets.QDateTimeEdit()
        tMaxEdit.setCalendarPopup(True)
        tMaxEdit.setDateTimeRange(timestampMinMax[0], timestampMinMax[1])
        tMaxEdit.setDateTime(timestampMinMax[1])
        tMaxEdit.setDisplayFormat("yyyy-MM-dd hh:mm:ss")

        tMaxLabel = QtWidgets.QLabel("Maximal &time: ")
        tMaxLabel.setBuddy(tMaxEdit)

        s = ("Legal value: " + timestampMinMax[0].strftime("%Y-%m-%d %H:%M:%S") +
             " ~ " + timestampMinMax[1].strftime("%Y-%m-%d %H:%M:%S") +
             " " + timestampMinMax[0].strftime("%Z%z"))
        tDiscLabel = QtWidgets.QLabel(s)

        tMinEdit.dateTimeChanged.connect(lambda dt: tMaxEdit.setMinimumDateTime(dt))
        tMaxEdit.dateTimeChanged.connect(lambda dt: tMinEdit.setMaximumDateTime(dt))

        tMinLayout = QtWidgets.QHBoxLayout()
        tMinLayout.addWidget(tMinLabel)
        tMinLayout.addWidget(tMinEdit)

        tMaxLayout = QtWidgets.QHBoxLayout()
        tMaxLayout.addWidget(tMaxLabel)
        tMaxLayout.addWidget(tMaxEdit)

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

        self.setWindowTitle("Set Filters")
        self.setLayout(mainLayout)
        self.show()
