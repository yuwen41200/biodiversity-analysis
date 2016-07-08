#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from folium import Map


# noinspection PyPep8Naming
class LeafletMap:

    def __init__(self):
        """
        The following doesn't work.

        # Instead of writing to file, just write to memory
        def toHTML(self, **kwargs):
            return self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.leafletMap = folium.Map(location=[23.5236, 120.6750])
        html = self.leafletMap.toHTML()
        """
        self.mapLocation = os.getcwd() + os.path.sep + 'temp.html'

        mapResource = Map(location=[23.5236, 120.6750], zoom_start=13)
        mapResource.circle_marker(location=[23.5220, 120.6763], radius=350, popup='demo',
                                  line_color='#3186cc', fill_color='#3186cc')
        mapResource.save(self.mapLocation)

        self.webEngineView = QWebEngineView()
        self.webEngineView.load(QUrl(self.mapLocation))
