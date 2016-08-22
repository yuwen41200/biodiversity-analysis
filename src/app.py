#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import multiprocessing

from PyQt5.QtWidgets import QApplication

from model.dataset import Dataset
from view.main_window import MainWindow
from controller.main_action import MainAction
from controller.cooccurrence_calculation import CooccurrenceCalculation

if __name__ == '__main__':

    # QTBUG-49940 workaround.
    os.environ["LIBOVERLAY_SCROLLBAR"] = "0"

    # Fork a subprocess at the beginning to prevent crash.
    queue = multiprocessing.Queue()
    # noinspection PyArgumentList
    process = multiprocessing.Process(
        target=CooccurrenceCalculation.worker,
        args=(queue,),
        daemon=True
    )
    process.start()

    app = QApplication(sys.argv)
    MainAction(Dataset(), MainWindow(), process, queue)
    sys.exit(app.exec_())
