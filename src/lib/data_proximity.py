#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import itemgetter
from heapq import nsmallest
from collections import defaultdict

from lib.correlation_calculator import CorrelationCalculator


# noinspection PyPep8Naming
class DataProximity:

    def __init__(self, dataset, percentage=0.7):
        """
        Initialize data proximity calculator.

        :param dataset: Dataset model.
        :param percentage: The number of records taken into account when calculating species
                           ranking.
        """

        self.temporalData = dataset.temporalData
        self.spatialData = dataset.spatialData
        self.calculatedResult = []
        self.rankTakePercentage = percentage

    def extractDataset(self):
        """
        Extract dataset into a list of tuple of (key, timestamp, coordinate).

        :return: List of tuple of (key, timestamp, coordinate).
        """

        results = [(k, self.temporalData[k][i][0].timestamp(), u[0])
                   for k, coords in self.spatialData.items()
                   for i, u in enumerate(coords)]
        return results

    @staticmethod
    def recordRank(dataset, number=0, sortByDistance=True):
        """
        Rank pairs of records by distance, temporally and then spatially.

        :param dataset: List of tuple of (key, timestamp, coordinate).
        :param number: The number of pairs of records to return.
        :param sortByDistance: Whether to sort by distance or by time difference.
        :return: List of pairs of ``Data``, where ``Data`` is tuple of (time difference, distance,
                 index of first element in dataset, index of second element in dataset).
        """

        total = len(dataset)

        if not number:
            number = total

        dist = CorrelationCalculator.distance

        # Calculate timestamp difference and distance between every pair of records.
        # Ignore those pairs within the same species.
        pairs = [(dist(dataset[i][2], dataset[j][2]), abs(dataset[i][1] - dataset[j][1]), i, j)
                 for i in range(len(dataset)) for j in range(i+1)
                 if dataset[i][0] != dataset[j][0]]

        number = int(number)
        if number > total*0.5:
            if sortByDistance:
                pairs.sort()
            else:
                pairs.sort(key=itemgetter(1, 0))
            return pairs

        # Use heap sort.
        if sortByDistance:
            return nsmallest(number, pairs)
        return nsmallest(number, pairs, key=itemgetter(1, 0))

    def speciesRank(self, onlyTake=0, temporalWeight=0.5, spatialWeight=0.5):
        """
        Calculate the correlation ranking of species.

        :param onlyTake: The number of records to return; it not supplied, return all records.
        :param temporalWeight: The weight of preference of time difference.
        :param spatialWeight: The weight of preference of distance.
        :return: List of tuples of ``Data``, where ``Data`` is a tuple of (score, (species 1,
                 species 2)).
        """

        dataset = self.extractDataset()
        sortByDistance = spatialWeight > temporalWeight
        recordRankResult = self.recordRank(
            dataset,
            len(dataset) * self.rankTakePercentage,
            sortByDistance
        )

        if len(recordRankResult) is 0:
            return []

        maxDistance = max(recordRankResult, key=lambda r: r[0])[0]
        maxTimeDiff = max(recordRankResult, key=lambda r: r[1])[1]
        totalWeight = temporalWeight+spatialWeight
        assert(totalWeight > 0)

        spatialWeight = 1.0 if maxDistance == 0 else spatialWeight / totalWeight
        temporalWeight = 1.0 if maxTimeDiff == 0 else temporalWeight / totalWeight
        spaceNormalizationFactor = 0.0 if maxDistance == 0 else spatialWeight / maxDistance
        timeNormalizationFactor = 0.0 if maxTimeDiff == 0 else temporalWeight / maxTimeDiff

        # Normalize temporal/spatial distance to [0, 1].
        scores = [r[0] * spaceNormalizationFactor + r[1] * timeNormalizationFactor
                  for r in recordRankResult]

        speciesPairs = defaultdict(float)
        count = defaultdict(int)
        for i in range(len(scores)):
            species1 = dataset[recordRankResult[i][2]][0]
            species2 = dataset[recordRankResult[i][3]][0]
            key = (species1, species2) if species1 > species2 else (species2, species1)
            speciesPairs[key] += scores[i]
            count[key] += 1

        assert(isinstance(onlyTake, int))
        averagedScores = [(score/count[key], key) for key, score in speciesPairs.items()]
        return (nsmallest(onlyTake, averagedScores)
                if onlyTake and onlyTake < len(averagedScores)
                else sorted(averagedScores))
