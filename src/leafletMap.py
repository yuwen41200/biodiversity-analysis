#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import folium
# noinspection PyUnresolvedReferences
from OpenGL import GL
# noinspection PyUnresolvedReferences
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datasetProcessor import randomEstimateLocation


# noinspection PyPep8Naming
class LeafletMap:


    def __init__(self, tiles="OpenStreetMap", centerCoordinate=(23.5, 120), zoom=3):
        """
        Initialize folium map.

        :param tiles: Tile source, defaults to OpenStreetMap.
        :param centerCoordinate: Coordinate of central point in map.
        :param zoom: Zoom level, defaults to 3.
        """

        # Instead of writing to file, just write to memory
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.webView = QWebEngineView()
        self.tiles = tiles
        self.zoom = zoom
        self.fMap = folium.Map(location=centerCoordinate, zoom_start=zoom, tiles=tiles)
        self.markerColors = {
            "#142b44", "#1d508d", "#297cbb", "#288ad6", "#0fdebd", "#16c98d", "#feef6d",
            "#ffc83f", "#fa5e5b", "#bf538d", "#841e1b", "#582c2b", "#2c3643", "#2c3643"
        }
        self.speciesMarkerColor = {}

        # Ignore simple_marker/circle_marker future warning
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)

    def refreshMap(self, dataset=None, selectedSpecies=[], centerCoordinate=None):
        """
        Rerender folium map, given a list of species.

        :param dataset: Dictionary of {species name -> list of coordinates}.
        :param selectedSpecies: List of names of selected species.
        :param centerCoordinate: Coordinate of central point in map.
        :return: None.
        """

        if dataset is None:
            dataset = {}

        if dataset and not centerCoordinate:
            allCoordinates = []
            for species, coordinates in dataset.items():
                if species in selectedSpecies:
                    allCoordinates += coordinates
            centerCoordinate = randomEstimateLocation(allCoordinates)

        if centerCoordinate:
            zoom = self.zoom + 3
            self.fMap = folium.Map(location=centerCoordinate, zoom_start=zoom, tiles=self.tiles)
        else:
            self.fMap = folium.Map(location=(23.5, 120), zoom_start=self.zoom, tiles=self.tiles)

        self.updateSpeciesMarkerColor(selectedSpecies)

        for species, coordinates in dataset.items():
            if species in selectedSpecies:
                for coordinate in coordinates:
                    self.fMap.circle_marker(
                            popup=species,
                            location=coordinate,
                            radius=400,
                            line_color=self.speciesMarkerColor[species],
                            fill_color="#cfcbaf",
                            fill_opacity=1
                        )

        # Render to LeafletMap.webView
        html = self.fMap.toHTML()
        self.webView.setHtml(html)

    def updateSpeciesMarkerColor(self, selectedSpecies):
        """
        Update the correspondence between species and their colors

        :param selectedSpecies: List of names of selected species.
        :return: None.
        """
        cur, prev = set(selectedSpecies), set(self.speciesMarkerColor.keys())
        common = cur.intersection(prev)

        import random
        for newSpecies in cur - common:
            color = self.markerColors.pop()
            self.speciesMarkerColor[newSpecies] = color

        for removedSpecies in prev - common:
            del self.speciesMarkerColor[removedSpecies]

