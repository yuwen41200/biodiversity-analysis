#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random


class Species:

    nColor = 14
    colors = [
        "#142b44", "#1d508d", "#297cbb", "#288ad6", "#0fdebd", "#16c98d", "#feef6d",
        "#ffc83f", "#fa5e5b", "#bf538d", "#841e1b", "#582c2b", "#2c3643", "#2c3643"
    ]

    def __init__(self):
        """
        Register a new species, give it a unique color.
        """

        assert Species.colors
        random.shuffle(Species.colors)
        self.color = Species.colors.pop()

    @staticmethod
    def available():
        """
        Check how many colors are currently available.

        :return: The number of available colors.
        """

        return len(Species.colors)

    def __del__(self):
        """
        Delete the species, restore its color.

        :return: None.
        """

        Species.colors.append(self.color)
