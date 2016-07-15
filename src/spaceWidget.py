#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout


# noinspection PyPep8Naming
class SpaceWidget(QWidget):

    # noinspection PyArgumentList
    def __init__(self, webView):
        """
        Construct the Space page in the main window.
        A LeafletMap.webView will be shown on this page.

        :param webView: The LeafletMap.webView widget.
        """

        super().__init__()
        self.view = webView

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.view)

        self.setLayout(mainLayout)
