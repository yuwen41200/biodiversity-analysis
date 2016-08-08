#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class ScatterPlot:

    def __init__(self, dataset):
        """
        Initialize the matplotlib plot.

        :param dataset: Dataset model.
        """

        figure = Figure()
        self.mplCanvas = FigureCanvasQTAgg(figure)
        axes = figure.add_subplot(111)
        axes.hold(False)
        a = numpy.arange(0.0, 3.0, 0.01)
        b = numpy.sin(2 * numpy.pi * a)
        color = [0.003 * _a / 0.003 * _a for _a in a]
        size = [(15 * _b / (b[0] + 1.732)) ** 2 for _b in b]
        axes.scatter(a, b, c=color, s=size, alpha=0.5, edgecolors='face')
        axes.set_xlabel(r'$\Delta_i$', fontsize=20)
        axes.set_ylabel(r'$\Delta_{i+1}$', fontsize=20)
        axes.grid(True)
        figure.tight_layout()
        self.mplCanvas.draw()
