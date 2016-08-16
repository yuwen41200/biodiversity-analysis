#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy, QDesktopWidget


class ScatterPlot:

    def __init__(self, dataset):
        """
        Initialize the matplotlib plot.

        :param dataset: Dataset model.
        """

        self.temporalData = dataset.temporalData
        self.selectedSpecies = dataset.selectedSpecies

        self.figure = Figure()
        self.mplCanvas = FigureCanvasQTAgg(self.figure)
        self.mplCanvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mplCanvas.updateGeometry()
        self.mplCanvas.setMinimumHeight(QDesktopWidget().availableGeometry().height() * 0.64)
        self.mplCanvas.setStatusTip(
            "Hour ranges from 0 (inclusive) to 24 (exclusive). "
            "Month ranges from 1 (inclusive) to 13 (exclusive)."
        )
        self.minYear, self.maxYear = 1000000, 0
        self.axes = self.figure.add_subplot(111)
        self.axes.hold(False)

        self.rebuild()

    def rebuild(self):
        """
        Rebuild the matplotlib plot.

        :return: None.
        """

        months, years, colors, sizes = [], [], [], []
        for key, value in self.selectedSpecies.items():
            for timestamp, amount in self.temporalData[key]:
                month = timestamp.month + (timestamp.day - 1) / 31
                year = timestamp.year
                months.append(month)
                years.append(year)
                colors.append(value.color)
                sizes.append(128 * (amount ** 0.5) + 128)

        minYear, maxYear = self.getYearRange(self.temporalData)
        self.axes.scatter(months, years, c=colors, s=sizes, alpha=0.5, edgecolors="face")
        self.axes.set_xlabel("Months")
        self.axes.set_ylabel("Years")
        self.axes.set_xticks(list(range(1, 14)))
        self.axes.set_yticks(list(range(minYear-1, maxYear+2)))
        self.axes.set_xlim(1, 13)
        self.axes.set_ylim(minYear-1, maxYear+1)
        self.axes.grid(True)
        self.axes.ticklabel_format(useOffset=False)
        self.figure.tight_layout()
        self.mplCanvas.draw()

    def getYearRange(self, temporalData):
        """
        Get the maximum and minimum year in the dataset

        :param temporalData: Temporal dataset.
        :return: (minimum year, maximum year).
        """

        # do not calculate if it's been done
        if len(temporalData) and self.maxYear is 0:
            years = [t[0].year for ts in temporalData.values() for t in ts]
            minY, maxY = 1000000, 0
            for year in years:
                if year > maxY:
                    maxY = year
                if year < minY:
                    minY = year
            # cache the result
            self.minYear, self.maxYear = minY, maxY
        return self.minYear, self.maxYear

