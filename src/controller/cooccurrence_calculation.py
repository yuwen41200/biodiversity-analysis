#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from queue import Empty
from threading import Lock

from PyQt5.QtCore import QTimer

from lib.data_proximity import DataProximity


# noinspection PyPep8Naming
class CooccurrenceCalculation:

    STATUS = Enum("STATUS", ("IDLE", "RUNNING", "FINISHED"))

    # noinspection PyUnresolvedReferences
    def __init__(self, dataset, cooccurrenceAnalysisWidget, process, queue):
        """
        Initialize the controller for the co-occurrence correlation quotient table.

        :param dataset: Dataset model.
        :param cooccurrenceAnalysisWidget: CooccurrenceAnalysisWidget view.
        :param process: Worker subprocess.
        :param queue: Message queue for the worker subprocess.
        """

        self.queue = queue
        self.process = process
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

    def activate(self):
        """
        Do the calculations in another process.

        :return: None.
        """

        with self.lock:
            if not self.dataset.spatialData:
                return

            elif self.status == self.STATUS.IDLE:
                self.queue.put(self.dataset)
                self.queue.put(self.widget.limit)
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
    def worker(queue):
        """
        Calculate the co-occurrence correlation quotient.

        :param queue: A ``multiprocessing.Queue`` object to communicate between processes.
        :return: None.
        """

        dataset = queue.get()
        limit = queue.get()

        parent = super(dataset.spatialData.__class__, dataset.spatialData)
        for key in dataset.spatialData:
            parent.__setitem__(key, dataset.spatialData[key][0])

        parent = super(dataset.temporalData.__class__, dataset.temporalData)
        for key in dataset.temporalData:
            parent.__setitem__(key, dataset.temporalData[key][0])

        dataProximity = DataProximity(dataset)
        results = dataProximity.speciesRank(limit)
        msg = [(r[1][0], r[1][1], r[0]) for r in results]
        queue.put(msg)
