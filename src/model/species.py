#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Species:

    nColor = 14
    colors = [
        "#bf538d", "#67747c", "#142b44", "#ffc83f", "#297cbb", "#ff4500", "#0003ff",
        "#ff003b", "#9700ff", "#ff3d66", "#4400ff", "#841e1b", "#069900", "#e0000f"
    ]

    def __init__(self):
        """
        Register a new species, give it a unique color.
        """

        assert Species.colors
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
