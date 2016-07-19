#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import folium
# noinspection PyUnresolvedReferences
from OpenGL import GL
# noinspection PyUnresolvedReferences
from PyQt5.QtWebEngineWidgets import QWebEngineView
from datasetProcessor import randomEstimateLocation


# noinspection PyPep8Naming
class LeafletMap:

    def __init__(self, tiles="OpenStreetMap", centerCoordinate=(23.5, 120), zoom=4):
        """
        Initialize folium map.

        :param tiles: Tile source, defaults to OpenStreetMap.
        :param centerCoordinate: Coordinate of central point in map.
        :param zoom: Zoom level, defaults to 3.
        """

        # Instead of writing to file, just write to memory
        def toHTML(_self, **kwargs):
            return _self.get_root().render(**kwargs)
        folium.element.Element.toHTML = toHTML

        self.webView = QWebEngineView()
        self.tiles = tiles
        self.zoom = zoom
        self.defaultCenterCoordinate = centerCoordinate
        self.centerCoordinate = None

        # Ignore circle_marker future warnings
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)

    def addSpecies(self, dataset, species, selectedSpecies):
        """
        Add a new species to folium map.

        :param dataset: Dictionary of {species name: list of coordinates}.
        :param species: Name of the species to be added.
        :param selectedSpecies: Dictionary of {selected species name: its Species object}.
        :return: None.
        """

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

        if len(selectedSpecies) > 1:
            self.refresh(dataset, rebuild=False)
        else:
            self.refresh(dataset, rebuild=True)

    def refresh(self, dataset={}, rebuild=True):
        """
        Rerender folium map.

        :param dataset: Dictionary of {species name: list of coordinates}.
        :param rebuild: whether or not to rebuild the whole map
        :return: None.
        """

        if dataset:
            if not self.centerCoordinate:
                allCoordinates = sum(dataset.values(), [])
                self.centerCoordinate = randomEstimateLocation(allCoordinates)

            if rebuild:
                self.fMap = folium.Map(location=self.centerCoordinate, zoom_start=self.zoom + 4, tiles=self.tiles)
        else:
            self.fMap = folium.Map(location=self.defaultCenterCoordinate, zoom_start=self.zoom, tiles=self.tiles)

        # Render to LeafletMap.webView
        html = self.fMap.toHTML()
        self.webView.setHtml(html)
