#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from multiprocessing import Process, Queue
from queue import Empty
from time import sleep


# noinspection PyPep8Naming
class CooccurrenceCalculation:

    STATUS = Enum("STATUS", ("IDLE", "RUNNING", "FINISHED"))

    def __init__(self, dataset, cooccurrenceAnalysisWidget):
        """
        Initialize the controller for the co-occurrence quotient table.

        :param dataset: Dataset model.
        :param cooccurrenceAnalysisWidget: CooccurrenceAnalysisWidget view.
        """

        self.queue = Queue()
        self.widget = cooccurrenceAnalysisWidget
        self.status = self.STATUS.IDLE

    # noinspection PyArgumentList
    def active(self):
        """
        Do the calculations in another process. |br|
        Triggered when the active page in the main window changed.

        :return: None.
        """

        if self.status == self.STATUS.IDLE:
            process = Process(target=self.calculate, args=(self.queue,), daemon=True)
            process.start()
            self.widget.addSpeciesToTable("Calculating...", "Please come back later.", 0)
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
                self.status = self.STATUS.FINISHED

    @staticmethod
    def calculate(queue):
        """
        <<< TODO >>> |br|
        Calculate co-occurrence quotient.

        :param queue: A ``multiprocessing.Queue`` object to communicate between processes.
        :return: None.
        """

        sleep(10)
        queue.put([("foo", "bar", 87.0), ("bah", "yee", 0.879487)])
