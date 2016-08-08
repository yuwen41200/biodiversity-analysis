#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy


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
        self.axes = self.figure.add_subplot(111)
        self.axes.hold(False)

        self.rebuild()

    def rebuild(self):
        """
        Rebuild the matplotlib plot.

        :return: None.
        """

        months, hours, colors, sizes = [], [], [], []
        for key, value in self.selectedSpecies.items():
            for timestamp, amount in self.temporalData[key]:
                months.append(timestamp.month)
                hours.append(timestamp.hour)
                colors.append(value.color)
                sizes.append(amount << 4 ** 2)

        self.axes.scatter(hours, months, c=colors, s=sizes, alpha=0.5, edgecolors="face")
        self.axes.set_xlabel("Hour")
        self.axes.set_ylabel("Month")
        self.axes.grid(True)
        self.figure.tight_layout()
        self.mplCanvas.draw()
