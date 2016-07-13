#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import folium
from OpenGL import GL
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# noinspection PyPep8Naming
class LeafletMap:

    def __init__(self,
                 tiles="OpenStreetMap",
                 location=[23.5,120],
                 zoom=3):

        # Instead of writing to file, just write to memory
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.webView = QWebEngineView()
        self.tiles = tiles
        self.leafletMap = folium.Map(location=location,
                                     zoom_start=zoom,
                                     tiles=tiles)


    def refreshMap(self, speciesList={}, centerCoordinate=None):
        """
        Re-render folium map, given a list of species.

        :param speciesList: dictionary of {species name -> list of location}.
        :param centerCoordinate: coordinate of central point in map.
        :return: None.
        """

        if centerCoordinate:
            self.leafletMap = folium.Map(location=centerCoordinate,
                                         tiles=self.tiles)

        for name, places in speciesList.items():
            for place in places:
                self.leafletMap.simple_marker(location=place, popup=name)

        # render to webview
        html = self.leafletMap.toHTML()
        self.webView.setHtml(html)
