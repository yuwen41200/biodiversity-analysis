#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datasetProcessor import extractCsv
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium



class Map:

    def __init__(self):
        # Instead of writing to file, just write to memory
        def toHTML(self, **kwargs):
            return self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.webview = QWebEngineView()

    def refreshMap(self, darwinCoreData):
        fields, data = extractCsv(darwinCoreData, ["decimalLatitude", "decimalLongitude"])

    def renderView(self):
        html = self.leafletMap.toHTML()
        self.webview.setHtml(html)
