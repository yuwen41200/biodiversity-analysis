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

    def __init__(self, dataset, tiles="OpenStreetMap", centerCoordinate=(23.5, 120), zoom=4):
        """
        Initialize the folium map.

        :param dataset: Dataset model.
        :param tiles: Tile source, defaults to OpenStreetMap.
        :param centerCoordinate: Coordinate of central point in map, defaults to (23.5, 120).
        :param zoom: Zoom level, defaults to 4.
        """

        self.dataset = dataset.dataset
        self.selectedSpecies = dataset.selectedSpecies

        # Instead of writing to file, just write to memory.
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.location = centerCoordinate
        self.zoom = zoom
        self.tiles = tiles

        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.fMap = None
        self.rebuild()

        # Ignore ``folium.Map.circle_marker()`` future warnings.
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)

    def add(self, newSpecies):
        """
        Add a new species to the folium map.

        :param newSpecies: Name of the new species to be added.
        :return: None.
        """

        if len(self.selectedSpecies) <= 1:
            self.rebuild()

        for coordinate in self.dataset[newSpecies]:
            color = self.selectedSpecies[newSpecies].color
            self.fMap.circle_marker(
                popup=newSpecies,
                location=coordinate,
                radius=150,
                line_color=color,
                fill_color=color,
                fill_opacity=1
            )

        self.refresh()

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

        if self.dataset:
            allCoordinates = sum(self.dataset.values(), [])
            centerCoordinate = DatasetProcessor.randomEstimateLocation(allCoordinates)
            zoom = self.zoom + 4
            self.fMap = folium.Map(location=centerCoordinate, zoom_start=zoom, tiles=self.tiles)

        else:
            self.fMap = folium.Map(location=self.location, zoom_start=self.zoom, tiles=self.tiles)
