#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium



class Map:

    def __init__(self):
        # Instead of writing to file, just write to memory
        def toHTML(self, **kwargs):
            return self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.leafletMap = folium.Map(location=[23.5236, 120.6750])
        html = self.leafletMap.toHTML()
