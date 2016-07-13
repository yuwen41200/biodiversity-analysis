#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import folium
# noinspection PyUnresolvedReferences
from OpenGL import GL
# noinspection PyUnresolvedReferences
from PyQt5.QtWebEngineWidgets import QWebEngineView


# noinspection PyPep8Naming
class LeafletMap:

    def __init__(self, tiles="OpenStreetMap", location=None, zoom=3):
        if location is None:
            location = [23.5, 120]

        # Instead of writing to file, just write to memory
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.webView = QWebEngineView()
        self.webView.setStatusTip("Drag to change the displayed region.")
        self.tiles = tiles
        self.leafletMap = folium.Map(location=location, zoom_start=zoom, tiles=tiles)

    def refreshMap(self, speciesData=None, centerCoordinate=None):
        """
        Re-render folium map, given a list of species.

        :param speciesData: dictionary of {species name -> list of location}.
        :param centerCoordinate: coordinate of central point in map.
        :return: None.
        """

        if speciesData is None:
            speciesData = {}

        if centerCoordinate:
            self.leafletMap = folium.Map(location=centerCoordinate, tiles=self.tiles)

        for name, places in speciesData.items():
            for place in places:
                self.leafletMap.simple_marker(location=place, popup=name)

        # Render to `LeafletMap.webView`
        html = self.leafletMap.toHTML()
        self.webView.setHtml(html)
