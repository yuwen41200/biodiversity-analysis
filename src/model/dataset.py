#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.multi_dict import MultiDict


class Dataset:
    """
    Store program data here.

    :var self.spatialData: Dictionary of {species name: list of (coordinate, amount) tuples}. |br|
                           Coordinate is a (y-coordinate, x-coordinate) tuple.
    :var self.temporalData: Dictionary of {species name: list of (timestamp, amount) tuples}. |br|
                            Timestamp is a Python datetime object.
    :var self.auxiliaryData: Dictionary of {species name: its vernacular name}.
    :var self.selectedSpecies: Dictionary of {selected species name: its Species object}.
    """

    def __init__(self):
        """
        Initialize the dataset.
        """

        self.spatialData = MultiDict()
        self.temporalData = MultiDict()
        self.auxiliaryData = dict()
        self.selectedSpecies = {}

    @staticmethod
    def license():
        """
        Return the license of this program.

        :return: The license, in HTML format.
        """

        return (
            "<h1>Biodiversity Analysis</h1>"
            "<p><b>Biodiversity Data Analysis and Visualization</b><br>"
            "Copyright (C) 2016 Yu-wen Pwu and Yun-chih Chen<br>"
            "<a href='https://github.com/yuwen41200/biodiversity-analysis'>"
            "https://github.com/yuwen41200/biodiversity-analysis</a></p>"
            "<p>This program is free software: you can redistribute it and/or modify "
            "it under the terms of the GNU General Public License as published by "
            "the Free Software Foundation, either version 3 of the License, or "
            "(at your option) any later version.</p>"
            "<p>This program is distributed in the hope that it will be useful, "
            "but WITHOUT ANY WARRANTY; without even the implied warranty of "
            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
            "GNU General Public License for more details.</p>"
            "<p>You should have received a copy of the GNU General Public License "
            "along with this program. If not, see <a href='http://www.gnu.org/licenses/'>"
            "http://www.gnu.org/licenses/</a>.</p>"
            "<p>&nbsp;</p>"
        )
