#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal


# noinspection PyPep8Naming
class ClickableLabel(QtWidgets.QLabel):

    labelClicked = pyqtSignal(str, name="labelClicked")

    # noinspection PyArgumentList
    def __init__(self, *args, **kwargs):
        """
        Customize a clickable QLabel.

        :param args: Arguments for the QLabel.
        :param kwargs: Keyword arguments for the QLabel.
        """

        super().__init__(*args, **kwargs)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Emit signal ``ClickableLabel.labelClicked()`` when clicked. |br|
        The signal contains one argument, which is the label's text. |br|
        This method overrides that in QLabel.

        :param mouseEvent: A QMouseEvent object.
        :return: None.
        """

        self.labelClicked.emit(self.text())
