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
                month = timestamp.month + (timestamp.day - 1) / 31
                hour = timestamp.hour + timestamp.minute / 60
                months.append(month)
                hours.append(hour)
                colors.append(value.color)
                sizes.append(128 * (amount ** 0.5) + 128)

        self.axes.scatter(hours, months, c=colors, s=sizes, alpha=0.5, edgecolors="face")
        self.axes.set_xlabel("Hour")
        self.axes.set_ylabel("Month")
        self.axes.set_xticks(list(range(0, 25)))
        self.axes.set_yticks(list(range(1, 14)))
        self.axes.set_xlim(0, 24)
        self.axes.set_ylim(1, 13)
        self.axes.grid(True)
        self.figure.tight_layout()
        self.mplCanvas.draw()
