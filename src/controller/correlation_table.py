#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.correlation_calculator import CorrelationCalculator


# noinspection PyPep8Naming
class CorrelationTable:

    def __init__(self, dataset, spatialAnalysisWidget):
        """
        Initialize the controller for the correlation quotient table.

        :param dataset: Dataset model.
        :param spatialAnalysisWidget: SpatialAnalysisWidget view.
        """

        self.dataset = dataset.dataset
        self.selectedSpecies = dataset.selectedSpecies
        self.spatialTable = spatialAnalysisWidget

    def add(self, newSpecies):
        """
        Insert all possible combinations into the correlation quotient table.

        :param newSpecies: Name of the new species to be added.
        :return: None.
        """

        self.spatialTable.disableAutoSort()
        for species in self.selectedSpecies:
            if species != newSpecies:
                similarity = CorrelationCalculator.calculateSimilarity(
                    self.dataset[newSpecies], self.dataset[species]
                )
                self.spatialTable.addSpeciesToTable(newSpecies, species, similarity)
        self.spatialTable.enableAutoSort()
