#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import cos

def calculateSimilarity(groupA, groupB):
    """
    Calculate the Hausdorff distance between two groups of coordinates
    See http://goo.gl/ik71mP

    :param groupA: list of coordinates
    :param groupB: list of coordinates
    :return: Hausdorff distance
    """
    distances = [ [distance(a, b) for a in groupA] for b in groupB ]
    h1 = max(map(min, distances))
    h2 = max([ min([ds[i] for ds in distances]) for i in range(len(groupA)) ])
    return max(h1,h2)

def distance(p1, p2):
    """
    Calculate the _relative_ distance between two coordinate
    See http://goo.gl/4VSrg6

    :param p1: point 1 (latitude,longitude)
    :param p2: point 2 (latitude,longitude)
    :return: relative distance
    """
    lat1, lon1 = p1
    lat2, lon2 = p2
    return cos(lat1 * 0.01745) * cos(lat2 * 0.01745) * (1 - cos((lon2 - lon1) * 0.01745)) \
           - cos((lat2 - lat1) * 0.01745)
