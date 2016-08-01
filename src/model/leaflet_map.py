#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import folium
# noinspection PyUnresolvedReferences
from OpenGL import GL
# noinspection PyUnresolvedReferences
from PyQt5 import QtWebEngineWidgets

from lib.dataset_processor import DatasetProcessor


# noinspection PyPep8Naming
class LeafletMap:

    tiles = {
        "Landscape": (
            'http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png',
            '&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, '
            '<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        ),
        "Grayscale": (
            'http://server.arcgisonline.com/ArcGIS/rest/services/Canvas/'
            'World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
            'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ'
        )
    }

    def __init__(self, dataset, tile="OpenStreetMap", centerCoordinate=(23.5, 120), zoom=4):
        """
        Initialize the folium map.

        :param dataset: Dataset model.
        :param tile: Tile source, defaults to OpenStreetMap.
        :param centerCoordinate: Coordinate of central point in map, defaults to (23.5, 120).
        :param zoom: Zoom level, defaults to 4.
        """

        self.spatialData = dataset.spatialData
        self.selectedSpecies = dataset.selectedSpecies

        # Instead of writing to file, just write to memory.
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.location = centerCoordinate
        self.zoom = zoom

        if tile not in self.tiles:
            self.tile = tile
            self.attr = None
        else:
            self.tile = self.tiles[tile][0]
            self.attr = self.tiles[tile][1]

        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.webView.setStatusTip("Drag to change the displayed region.")
        self.fMap = None

        self.rebuild()
        self.refresh()

        # Ignore ``folium.Map.circle_marker()`` future warnings.
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)

    def add(self, newSpecies):
        """
        Add a new species to the folium map.

        :param newSpecies: Name of the new species to be added.
        :return: None.
        """

        if len(self.selectedSpecies) == 1:
            self.rebuild()

        for coordinate, amount in self.spatialData[newSpecies]:
            color = self.selectedSpecies[newSpecies].color
            self.fMap.circle_marker(
                popup=newSpecies,
                location=coordinate,
                radius=amount*100,
                line_color=color,
                fill_color=color,
                fill_opacity=1
            )

    def remove(self):
        """
        Remove an old species from the folium map.

        :return: None.
        """

        if len(self.selectedSpecies) != 1:
            self.rebuild()

        for species in self.selectedSpecies:
            self.add(species)

    def refresh(self):
        """
        Refresh the folium map.

        :return: None.
        """

        html = self.fMap.toHTML()
        self.webView.setHtml(html)

    def rebuild(self):
        """
        Rebuild the folium map.

        :return: None.
        """

        if self.spatialData and self.selectedSpecies:
            coordinateList = [n[0] for m in self.spatialData for n in m]
            coordinateSum = sum(coordinateList, ())
            centerCoordinate = DatasetProcessor.randomEstimateLocation(coordinateSum)
            zoom = self.zoom + 4
            self.fMap = folium.Map(location=centerCoordinate, zoom_start=zoom,
                                   tiles=self.tile, attr=self.attr)

        else:
            self.fMap = folium.Map(location=self.location, zoom_start=self.zoom,
                                   tiles=self.tile, attr=self.attr)
