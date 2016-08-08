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

        figure = Figure(figsize=(5, 4), dpi=100)
        self.mplCanvas = FigureCanvasQTAgg(figure)
        axes = figure.add_subplot(111)
        axes.hold(False)
        t = numpy.arange(0.0, 3.0, 0.01)
        s = numpy.sin(2 * numpy.pi * t)
        axes.plot(t, s)
        self.mplCanvas.draw()
