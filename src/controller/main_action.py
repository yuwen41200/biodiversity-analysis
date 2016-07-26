#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from model.species import Species
from model.leaflet_map import LeafletMap
from model.scatter_plot import ScatterPlot
from view.spatial_analysis_widget import SpatialAnalysisWidget
from view.temporal_analysis_widget import TemporalAnalysisWidget
from view.add_species_dialog import AddSpeciesDialog
from controller.correlation_table import CorrelationTable
from lib.dataset_processor import DatasetProcessor


# noinspection PyPep8Naming
class MainAction:

    def __init__(self, dataset, mainWindow):
        """
        Initialize the controller for the main window.

        :param dataset: Dataset model.
        :param mainWindow: MainWindow view.
        """

        self.dataset = dataset.dataset
        self.selectedSpecies = dataset.selectedSpecies
        self.license = dataset.license

        self.map = LeafletMap(dataset)
        self.plot = ScatterPlot(dataset)
        spatial = SpatialAnalysisWidget(self.map.webView)
        temporal = TemporalAnalysisWidget(self.plot.mplCanvas)
        self.correlationTable = CorrelationTable(dataset, spatial, temporal)

        self.mainWindow = mainWindow
        self.mainWindow.setupWidgets(spatial, temporal, self)
        self.mainWindow.show()

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList, PyBroadException
    def importData(self):
        """
        Import data from a Darwin Core Archive (DwC-A) file. |br|
        Store them in ``Dataset.dataset``.

        :return: None.
        """

        title, extension = "Select a DwC-A File", "DwC-A File (*.zip)"
        filename = self.mainWindow.openFile(title, extension)

        if filename:
            try:
                darwinCoreData = DatasetProcessor.extractDarwinCoreArchive(filename)
                columns = ["decimalLatitude", "decimalLongitude", "scientificName"]
                dataList = DatasetProcessor.extractCsv(darwinCoreData, columns)[1]

            except:
                title = "Invalid DwC-A File"
                content = (
                    "The provided file is either not in DwC-A format or corrupted.\n"
                    "Please select a valid one."
                )
                self.mainWindow.alert(title, content, 3)
                return

            for r in dataList:
                self.dataset[r[2]] = (r[0], r[1])

            title = "Dataset Successfully Imported"
            content = "{:,d} records have been loaded.".format(len(dataList))
            self.mainWindow.alert(title, content, 0)

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def addSpecies(self):
        """
        Select a species from ``Dataset.dataset``, append it to ``Dataset.selectedSpecies``.

        :return: None.
        """

        if not self.dataset:
            title, content = "Empty Dataset", "Please import data first."
            self.mainWindow.alert(title, content, 3)

        elif not Species.available():
            title = "Too Many Species"
            content = ("Selecting more than " + str(Species.nColor) +
                       " species is not supported.")
            self.mainWindow.alert(title, content, 3)

        else:
            species = [k for k in self.dataset.keys() if k not in self.selectedSpecies]

            dialog = AddSpeciesDialog(species)
            dialog.exec_()
            newSpecies = dialog.newSpecies

            if newSpecies:
                self.selectedSpecies[newSpecies] = Species()
                newColor = self.selectedSpecies[newSpecies].color
                self.mainWindow.addSpeciesToLayout(newSpecies, newColor)
                self.map.add(newSpecies)
                self.correlationTable.add(newSpecies)

    def clearData(self):
        """
        Clear ``Dataset.dataset`` and ``Dataset.selectedSpecies``.

        :return: None.
        """

        self.dataset.clear()
        self.mainWindow.removeSpeciesFromLayout(range(len(self.selectedSpecies)))
        self.map.rebuild()
        self.map.refresh()
        self.correlationTable.clear()
        self.selectedSpecies.clear()

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def about(self):
        """
        Show information about this program.

        :return: None.
        """

        title = "About Biodiversity Analysis"
        content = self.license()
        self.mainWindow.alert(title, content, 4)
