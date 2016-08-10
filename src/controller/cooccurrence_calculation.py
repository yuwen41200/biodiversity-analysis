#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from multiprocessing import Process, Queue
from queue import Empty

from lib.data_proximity import DataProximity


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
        self.dataset = dataset
        self.widget = cooccurrenceAnalysisWidget
        self.status = self.STATUS.IDLE

    # noinspection PyArgumentList
    def active(self):
        """
        Do the calculations in another process. |br|
        Triggered when the active page in the main window changed.

        :return: None.
        """

        if not self.dataset.spatialData:
            self.widget.removeSpeciesFromTable()
            self.status = self.STATUS.IDLE

        elif self.status == self.STATUS.IDLE:
            process = Process(target=self.calculate, args=(self.queue, self.dataset), daemon=True)
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
    def calculate(queue, dataset):
        """
        Calculate co-occurrence quotient.

        :param queue: A ``multiprocessing.Queue`` object to communicate between processes.
        :param dataset: Dataset model.
        :return: None.
        """

        dataProximity = DataProximity(dataset)
        results = dataProximity.speciesRank(20)
        msg = [(r[1][0], r[1][1], r[0]) for r in results]
        queue.put(msg)
