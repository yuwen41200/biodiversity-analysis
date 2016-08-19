#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from multiprocessing import Queue
from queue import Empty
from threading import Lock
from PyQt5.QtCore import QTimer

from lib.terminatable_thread import TerminatableThread
from lib.data_proximity import DataProximity


# noinspection PyPep8Naming
class CooccurrenceCalculation:

    STATUS = Enum("STATUS", ("IDLE", "RUNNING", "FINISHED"))

    # noinspection PyUnresolvedReferences
    def __init__(self, dataset, cooccurrenceAnalysisWidget):
        """
        Initialize the controller for the co-occurrence correlation quotient table.

        :param dataset: Dataset model.
        :param cooccurrenceAnalysisWidget: CooccurrenceAnalysisWidget view.
        """

        self.queue = None
        self.process = None
        self.dataset = dataset
        self.widget = cooccurrenceAnalysisWidget
        self.status = self.STATUS.IDLE
        self.lock = Lock()
        self.timer = QTimer(cooccurrenceAnalysisWidget)

        self.widget.cooccurrenceCalculation = self
        self.timer.timeout.connect(self.activate)

    def halt(self):
        """
        Terminate the calculations. |br|
        Redo them if they already started.

        :return: None.
        """

        if self.queue:
            self.queue.close()
        if self.process:
            self.process.terminate()
        self.widget.removeSpeciesFromTable()

        if self.status != self.STATUS.IDLE:
            self.status = self.STATUS.IDLE
            self.activate()

    # noinspection PyArgumentList
    def activate(self):
        """
        Do the calculations in another process.

        :return: None.
        """

        with self.lock:
            if not self.dataset.spatialData:
                return

            elif self.status == self.STATUS.IDLE:
                self.queue = Queue()
                self.process = TerminatableThread(
                    target=self.calculate,
                    args=(self.queue, self.dataset, self.widget.limit),
                    daemon=True
                )
                self.process.start()
                string = "Calculating (limited to " + str(self.widget.limit) + " rows) ..."
                self.widget.addSpeciesToTable(string, "Please come back later.", 0)
                self.status = self.STATUS.RUNNING

            elif self.status == self.STATUS.RUNNING:
                try:
                    results = self.queue.get(False)
                except Empty:
                    return
                else:
                    self.widget.removeSpeciesFromTable()
                    for r in results:
                        self.widget.addSpeciesToTable(*r)
                    self.queue.close()
                    self.process.terminate()
                    self.status = self.STATUS.FINISHED

    def onFocus(self):
        """
        Start calculating and set a timer to check its status periodically. |br|
        Triggered when the current page in the main window changes to "Co-occurrence Analysis".

        :return: None.
        """

        self.activate()
        # Emit ``QTimer.timeout()`` signal every 10 seconds.
        self.timer.start(10000)

    def onBlur(self):
        """
        Unset the timer. |br|
        Triggered when the current page in the main window leaves "Co-occurrence Analysis".

        :return: None.
        """

        self.timer.stop()

    @staticmethod
    def calculate(queue, dataset, limit):
        """
        Calculate co-occurrence quotient.

        :param queue: A ``multiprocessing.Queue`` object to communicate between processes.
        :param dataset: Dataset model.
        :param limit: Maximum number of rows returned.
        :return: None.
        """

        dataProximity = DataProximity(dataset)
        results = dataProximity.speciesRank(limit)
        msg = [(r[1][0], r[1][1], r[0]) for r in results]
        queue.put(msg)
