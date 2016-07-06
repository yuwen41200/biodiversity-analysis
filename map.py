#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from mock import patch
import folium

class Map:

    render_method = "folium.element.Element.save"

    def __init__(self):
        map_osm = folium.Map(location=[45.5236, -122.6750])
        #patch(self.render_method, side_effect=folium.Element.render).start()
        map_osm.save('/tmp/folium.html')

if __name__ == '__main__':
    m = Map()

