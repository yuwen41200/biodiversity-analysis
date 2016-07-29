#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

        self.dataset = dataset.dataset
        self.selectedSpecies = dataset.selectedSpecies
        self.spatialAnalysisWidget = spatialAnalysisWidget
        self.temporalAnalysisWidget = temporalAnalysisWidget

    def add(self, newSpecies):
        """
        Insert all possible combinations of the new species into the correlation quotient table.

        :param newSpecies: Name of the new species to be added.
        :return: None.
        """

        self.spatialAnalysisWidget.disableAutoSort()

        for species in self.selectedSpecies:
            if species != newSpecies:
                similarity = CorrelationCalculator.calculateSimilarity(
                    self.dataset[newSpecies], self.dataset[species]
                )
                self.spatialAnalysisWidget.addSpeciesToTable(
                    newSpecies, species, similarity
                )

        self.spatialAnalysisWidget.enableAutoSort()

    def remove(self, oldSpecies=None):
        """
        Delete all rows containing the specified species from the correlation quotient table. |br|
        If the old species is not given, clear the whole table.

        :param oldSpecies: Name of the old species to be removed.
        :return: None.
        """

        self.spatialAnalysisWidget.disableAutoSort()
        self.spatialAnalysisWidget.removeSpeciesFromTable(oldSpecies)
        self.spatialAnalysisWidget.enableAutoSort()
