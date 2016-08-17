#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum
from multiprocessing import Process, Queue
from queue import Empty
from threading import Lock, Timer

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
        self.lock = Lock()
        self.timer = None
        self.widget.cooccurrenceCalculation = self

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
                self.process = Process(
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

        def task():
            """
            Activate periodically.

            :return: None.
            """

            self.timer = Timer(10, task)
            self.timer.daemon = True
            self.timer.start()

            # May produce the following error because it manipulates the GUI from another thread.
            #    QObject::connect: Cannot queue arguments of type 'QVector<int>'
            #    (Make sure 'QVector<int>' is registered using qRegisterMetaType().)
            self.activate()

        task()

    def onBlur(self):
        """
        Unset the timer. |br|
        Triggered when the current page in the main window leaves "Co-occurrence Analysis".

        :return: None.
        """

        if self.timer:
            self.timer.cancel()

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
