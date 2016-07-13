#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import folium
# noinspection PyUnresolvedReferences
from OpenGL import GL
# noinspection PyUnresolvedReferences
from PyQt5.QtWebEngineWidgets import QWebEngineView


# noinspection PyPep8Naming
class LeafletMap:

    def __init__(self, tiles="OpenStreetMap", centerCoordinate=None, zoom=3):
        """
        Initialize folium map.

        :param tiles: Tile source, defaults to OpenStreetMap.
        :param centerCoordinate: Coordinate of central point in map.
        :param zoom: Zoom level, defaults to 3.
        """

        if centerCoordinate is None:
            centerCoordinate = [23.5, 120]

        # Instead of writing to file, just write to memory
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.webView = QWebEngineView()
        self.tiles = tiles
        self.leafletMap = folium.Map(location=centerCoordinate, zoom_start=zoom, tiles=tiles)

    def refreshMap(self, dataset=None, selectedSpecies=None, centerCoordinate=None):
        """
        Rerender folium map, given a list of species.

        :param dataset: Dictionary of {species name -> list of coordinates}.
        :param selectedSpecies: List of names of selected species.
        :param centerCoordinate: Coordinate of central point in map.
        :return: None.
        """

        if dataset is None:
            dataset = {}

        if centerCoordinate:
            self.leafletMap = folium.Map(location=centerCoordinate, tiles=self.tiles)

        for species, coordinates in dataset.items():
            if species in selectedSpecies:
                for coordinate in coordinates:
                    self.leafletMap.simple_marker(location=coordinate, popup=species)

        # Render to LeafletMap.webView
        html = self.leafletMap.toHTML()
        self.webView.setHtml(html)
