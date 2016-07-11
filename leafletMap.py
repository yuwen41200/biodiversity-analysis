#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import folium
from OpenGL import GL
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datasetProcessor import extractCsv


# noinspection PyPep8Naming
class LeafletMap:

    def __init__(self):
        # Instead of writing to file, just write to memory
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.webView = QWebEngineView()

    def refreshMap(self, darwinCoreData):
        fields, data = extractCsv(darwinCoreData, ["decimalLatitude", "decimalLongitude"])

    def renderView(self):
        html = self.leafletMap.toHTML()
        self.webView.setHtml(html)
