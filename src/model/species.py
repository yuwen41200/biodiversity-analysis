#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random


class Species:

    nColor = 14
    colors = [
        "#bf538d", "#67747c", "#142b44", "#1d508d", "#297cbb", "#288ad6", "#0fdebd",
        "#16c98d", "#684e79", "#ff708e", "#47a899", "#841e1b", "#582c2b", "#fa5e5b"
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
