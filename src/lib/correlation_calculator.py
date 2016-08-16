#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import cos, asin, sqrt

from scipy import stats


# noinspection PyPep8Naming
class CorrelationCalculator:

    @staticmethod
    def calculateSpatialSimilarity(groupA, groupB):
        """
        Calculate the Hausdorff distance between two groups of coordinates. |br|
        See http://goo.gl/ik71mP.

        :param groupA: List of coordinates.
        :param groupB: List of coordinates.
        :return: Hausdorff distance.
        """

        distances = [[CorrelationCalculator.distance(a, b) for a in groupA] for b in groupB]
        h1 = max(map(min, distances))
        h2 = max([min([ds[i] for ds in distances]) for i in range(len(groupA))])
        return max(h1, h2)

    @staticmethod
    def distance(p1, p2):
        """
        Calculate the distance between two coordinates. |br|
        See http://goo.gl/4VSrg6.

        :param p1: Point 1 in (latitude, longitude).
        :param p2: Point 2 in (latitude, longitude).
        :return: Relative distance.
        """

        lat1, lon1 = p1
        lat2, lon2 = p2
        # pi / 180 = 0.0174532925199433
        P = 0.0174532925199433

        val = 0.5 - cos((lat2 - lat1) * P)/2 + \
            cos(lat1 * P) * cos(lat2 * P) * \
            (1 - cos((lon2 - lon1) * P)) / 2

        # Diameter of Earth = 2 * 6371 = 12742 km
        return 12742 * asin(sqrt(val))

    @staticmethod
    def calculateTemporalSimilarity(groupA, groupB):
        """
        Calculate the Kolmogorov-Smirnov correlation between two groups of sample data. |br|
        The smaller, the better. |br|
        See https://goo.gl/DtTY7z.

        :param groupA: List of samples.
        :param groupB: List of samples.
        :return: Kolmogorov-Smirnov statistics.
        """

        return stats.ks_2samp(groupA, groupB)[0]
