#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtWidgets import QApplication

from model.dataset import Dataset
from view.main_window import MainWindow
from controller.main_action import MainAction

if __name__ == '__main__':
    # QTBUG-49940 workaround
    os.environ["LIBOVERLAY_SCROLLBAR"] = "0"

    app = QApplication(sys.argv)

    dataset = Dataset()
    mainWindow = MainWindow()
    MainAction(dataset, mainWindow)

    sys.exit(app.exec_())
