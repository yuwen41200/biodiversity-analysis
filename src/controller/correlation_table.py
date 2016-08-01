#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy import stats

from lib.correlation_calculator import CorrelationCalculator


# noinspection PyPep8Naming
class CorrelationTable:

    def __init__(self, dataset, spatialAnalysisWidget, temporalAnalysisWidget):
        """
        Initialize the controller for the correlation quotient table.

        :param dataset: Dataset model.
        :param spatialAnalysisWidget: SpatialAnalysisWidget view.
        :param temporalAnalysisWidget: TemporalAnalysisWidget view.
        """

        self.spatialData = dataset.spatialData
        self.temporalData = dataset.temporalData
        self.selectedSpecies = dataset.selectedSpecies

        self.spatialAnalysisWidget = spatialAnalysisWidget
        self.temporalAnalysisWidget = temporalAnalysisWidget

    # noinspection PyTypeChecker
    def add(self, newSpecies):
        """
        Insert all possible combinations of the new species into the correlation quotient table.

        :param newSpecies: Name of the new species to be added.
        :return: None.
        """

        self.spatialAnalysisWidget.disableAutoSort()
        self.temporalAnalysisWidget.disableAutoSort()

        for species in self.selectedSpecies:
            if species != newSpecies:
                sx = [r[0] for r in self.spatialData[newSpecies]]
                sy = [r[0] for r in self.spatialData[species]]
                tx = [r[0].timestamp() for r in self.temporalData[newSpecies]]
                ty = [r[0].timestamp() for r in self.temporalData[species]]

                if len(ty) > len(tx):
                    tx[len(tx):len(ty)] = [float('NaN')] * (len(ty) - len(tx))
                else:
                    ty[len(ty):len(tx)] = [float('NaN')] * (len(tx) - len(ty))

                sc = CorrelationCalculator.calculateSimilarity(sx, sy)
                tc = stats.spearmanr(tx, ty)[0]

                self.spatialAnalysisWidget.addSpeciesToTable(newSpecies, species, sc)
                self.temporalAnalysisWidget.addSpeciesToTable(newSpecies, species, tc)

        self.spatialAnalysisWidget.enableAutoSort()
        self.temporalAnalysisWidget.enableAutoSort()

    def remove(self, oldSpecies=None):
        """
        Delete all rows containing the specified species from the correlation quotient table. |br|
        If the old species is not given, clear the whole table.

        :param oldSpecies: Name of the old species to be removed.
        :return: None.
        """

        self.spatialAnalysisWidget.disableAutoSort()
        self.temporalAnalysisWidget.disableAutoSort()

        if oldSpecies is None:
            self.spatialAnalysisWidget.removeSpeciesFromTable()
            self.temporalAnalysisWidget.removeSpeciesFromTable()
        else:
            self.spatialAnalysisWidget.removeSpeciesFromTable(oldSpecies)
            self.temporalAnalysisWidget.removeSpeciesFromTable(oldSpecies)

        self.spatialAnalysisWidget.enableAutoSort()
        self.temporalAnalysisWidget.enableAutoSort()
