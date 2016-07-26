#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class ScatterPlot:

    def __init__(self, dataset):
        """
        Initialize the matplotlib plot.

        :param dataset: Dataset model.
        """

        self.mplCanvas = self.MplCanvas(width=5, height=4, dpi=100)

    class MplCanvas(FigureCanvasQTAgg):

        def __init__(self, width=5, height=4, dpi=100):

            fig = Figure(figsize=(width, height), dpi=dpi)

            self.axes = fig.add_subplot(111)
            self.axes.hold(False)
            self.compute_initial_figure()

            FigureCanvasQTAgg.__init__(self, fig)
            FigureCanvasQTAgg.setSizePolicy(
                self,
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding
            )
            FigureCanvasQTAgg.updateGeometry(self)

        def compute_initial_figure(self):

            t = numpy.arange(0.0, 3.0, 0.01)
            s = numpy.sin(2 * numpy.pi * t)
            self.axes.plot(t, s)
