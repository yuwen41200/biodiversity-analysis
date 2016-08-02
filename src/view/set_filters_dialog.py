#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


# noinspection PyPep8Naming
class SetFiltersDialog(QtWidgets.QDialog):

    # noinspection PyArgumentList
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

        self.setWindowTitle("Set Filters")
        self.show()
