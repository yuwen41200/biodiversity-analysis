#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import folium
from OpenGL import GL
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datasetProcessor import extractCsv


# noinspection PyPep8Naming
class LeafletMap:

    def __init__(self,
                 windowSize=[750,500],
                 tiles="Stamen Terrain"):

        assert(len(windowSize) == 2)

        # Instead of writing to file, just write to memory
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.webView = QWebEngineView()
        self.windowSize = windowSize
        self.tiles = tiles
        self.dataNum = 0


    def refreshMap(self, speciesList, centerCoordinate=None):
        """
        rerender folium map, given a list of species
        param: speciesList, dictionary of {specis name -> list of location}
        param: centerCoordinate, coordinate of central point in map
        """
        if not speciesList:
            return

        if not self.leafletMap
            self.leafletMap = folium.Map(location=centerCoordinate,
                                         tiles=self.tiles,
                                         width=self.windowSize[0],
                                         height=self.windowSize[1])

        for name, places in speciesList.items():
            for place in places:
                self.leafletMap.simple_marker(location=place, popup=name)

        # render to webview
        html = leafletMap.toHTML()
        self.webView.setHtml(html)
