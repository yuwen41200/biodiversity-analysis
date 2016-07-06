#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium



class Map:

    def __init__(self):
        # Instead of writing to file, just write to memory
        def to_html(self, **kwargs):
            return self.get_root().render(**kwargs)
        folium.element.Element.to_html = to_html

        map_osm = folium.Map(location=[23.5236, 120.6750])
        html = map_osm.to_html()

if __name__ == '__main__':
    m = Map()

