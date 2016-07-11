#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datasetProcessor import extractCsv
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium


# noinspection PyPep8Naming
class LeafletMap:

    def __init__(self,
                 windowSize=[750,500],
                 tiles="Stamen Terrain"):

        assert(len(windowSize) == 2)

        # Instead of writing to file, just write to memory
        def toHTML(self, **kwargs):
            return self.get_root().render(**kwargs)
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
        for specis, places in data:
            for place in places:
                self.leafletMap.simple_marker(location=place, popup=specis)

        # render to webview
        html = leafletMap.toHTML()
        self.webView.setHtml(html)
