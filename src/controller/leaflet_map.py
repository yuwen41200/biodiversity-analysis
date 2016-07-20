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

    def __init__(self, tiles="OpenStreetMap", centerCoordinate=(23.5, 120), zoom=3):
        """
        Initialize the folium map.

        :param tiles: Tile source, defaults to OpenStreetMap.
        :param centerCoordinate: Coordinate of central point in map, defaults to (23.5, 120).
        :param zoom: Zoom level, defaults to 3.
        """

        # Instead of writing to file, just write to memory.
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.tiles = tiles
        self.zoom = zoom
        self.fMap = folium.Map(location=centerCoordinate, zoom_start=zoom, tiles=tiles)

        # Ignore circle_marker future warnings.
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)

    def add(self, dataset, species, selectedSpecies, centerCoordinate=None):
        """
        Add a new species to the folium map.

        :param dataset: Dictionary of {species name: list of coordinates}.
        :param species: Name of the new species to be added.
        :param selectedSpecies: Dictionary of {selected species name: its Species object}.
        :param centerCoordinate: Coordinate of central point in map.
        :return: None.
        """

        if not centerCoordinate:
            centerCoordinate = DatasetProcessor.randomEstimateLocation(dataset[species])

        if centerCoordinate:
            zoom = self.zoom + 5
            self.fMap = folium.Map(location=centerCoordinate, zoom_start=zoom, tiles=self.tiles)
        else:
            self.fMap = folium.Map(location=(23.5, 120), zoom_start=self.zoom, tiles=self.tiles)

        for coordinate in dataset[species]:
            color = selectedSpecies[species].color
            self.fMap.circle_marker(
                popup=species,
                location=coordinate,
                radius=40,
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

        # Render to ``LeafletMap.webView``.
        html = self.fMap.toHTML()
        self.webView.setHtml(html)
