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
        Initialize the controller for the co-occurrence correlation quotient table.

        :param dataset: Dataset model.
        :param cooccurrenceAnalysisWidget: CooccurrenceAnalysisWidget view.
        """

        self.queue = None
        self.process = None
        self.dataset = dataset
        self.widget = cooccurrenceAnalysisWidget
        self.status = self.STATUS.IDLE

    def halt(self):
        """
        Terminate the calculations. |br|
        Redo them if they already started.

        :return: None.
        """

        if isinstance(self.queue, Queue):
            self.queue.close()
        if isinstance(self.process, Process):
            self.process.terminate()
        self.widget.removeSpeciesFromTable()

        if self.status != self.STATUS.IDLE:
            self.status = self.STATUS.IDLE
            self.active()

    # noinspection PyArgumentList
    def active(self):
        """
        Do the calculations in another process. |br|
        Triggered when the active page in the main window changes to "Co-occurrence Analysis".

        :return: None.
        """

        if not self.dataset.spatialData:
            return

        elif self.status == self.STATUS.IDLE:
            self.queue = Queue()
            self.process = Process(
                target=self.calculate,
                args=(self.queue, self.dataset, self.widget.limit),
                daemon=True
            )
            self.process.start()
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
                self.queue.close()
                self.process.terminate()
                self.status = self.STATUS.FINISHED

    @staticmethod
    def calculate(queue, dataset, limit):
        """
        Calculate co-occurrence quotient.

        :param queue: A ``multiprocessing.Queue`` object to communicate between processes.
        :param dataset: Dataset model.
        :param limit: Maximal number of rows returned.
        :return: None.
        """

        dataProximity = DataProximity(dataset)
        results = dataProximity.speciesRank(limit)
        msg = [(r[1][0], r[1][1], r[0]) for r in results]
        queue.put(msg)
