#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dateutil.parser import parse
from pprint import pformat
from traceback import format_exc

from model.dataset import Dataset
from model.species import Species
from model.leaflet_map import LeafletMap
from model.scatter_plot import ScatterPlot
from view.spatial_analysis_widget import SpatialAnalysisWidget
from view.temporal_analysis_widget import TemporalAnalysisWidget
from view.cooccurrence_analysis_widget import CooccurrenceAnalysisWidget
from view.set_filters_dialog import SetFiltersDialog
from view.add_species_dialog import AddSpeciesDialog
from controller.correlation_table import CorrelationTable
from controller.cooccurrence_calculation import CooccurrenceCalculation
from lib.dataset_processor import DatasetProcessor


# noinspection PyPep8Naming
class MainAction:

    def __init__(self, dataset, mainWindow, process, pipe):
        """
        Initialize the controller for the main window.

        :param dataset: Dataset model.
        :param mainWindow: MainWindow view.
        :param process: Worker subprocess.
        :param pipe: Message pipe for the worker subprocess.
        """

        self.spatialData = dataset.spatialData
        self.temporalData = dataset.temporalData
        self.auxiliaryData = dataset.auxiliaryData
        self.selectedSpecies = dataset.selectedSpecies

        self.map = LeafletMap(dataset, "Landscape")
        self.plot = ScatterPlot(dataset)
        spatial = SpatialAnalysisWidget(self.map.webView)
        temporal = TemporalAnalysisWidget(self.plot.mplCanvas)
        cooccurrence = CooccurrenceAnalysisWidget()
        self.correlationTable = CorrelationTable(dataset, spatial, temporal)
        self.cooccurrenceCalculation = CooccurrenceCalculation(
            dataset, cooccurrence, process, pipe
        )

        self.mainWindow = mainWindow
        self.mainWindow.setupWidgets(
            spatial, temporal, cooccurrence, self, self.cooccurrenceCalculation
        )
        self.mainWindow.show()

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList, PyBroadException
    def importData(self):
        """
        Import data from a Darwin Core Archive (DwC-A) file. |br|
        Store them in ``Dataset``.

        :return: None.
        """

        if self.spatialData:
            title = "Dataset Already Imported"
            content = "To import new data, please clear data first."
            self.mainWindow.alert(title, content, 3)
            return

        title, extension = "Select a DwC-A File", "DwC-A File (*.zip)"
        filename = self.mainWindow.openFile(title, extension)

        if filename:
            try:
                archiveData, archiveMeta = DatasetProcessor.extractDarwinCoreArchive(filename)

                if archiveMeta["coreType"] not in Dataset.supportedCores:
                    title = "Unsupported DwC Type"
                    content = (
                        "The provided file has core type of " + archiveMeta["coreType"] + ".\n"
                        "This program only support " + ", ".join(Dataset.supportedCores) + "."
                    )
                    self.mainWindow.alert(title, content, 3)
                    return

                columns = [
                    ("individualCount", True),
                    ("eventDate", True),
                    ("decimalLatitude", True),
                    ("decimalLongitude", True),
                    ("scientificName", True),
                    ("vernacularName", False)
                ]

                try:
                    dataList = DatasetProcessor.extractCsv(archiveData, archiveMeta, columns)
                except ValueError as e:
                    title = "Invalid DwC-A File"
                    content = str(e) + "\nPlease select a DwC-A file with such field."
                    self.mainWindow.alert(title, content, 3)
                    return

            except:
                title = "Invalid DwC-A File"
                content = (
                    "The provided file is either not in DwC-A format or corrupted.\n"
                    "Please select a valid one.\n\n"
                )
                self.mainWindow.alert(title, content + format_exc(), 3)
                return

            for r in dataList:
                try:
                    r0int = int(r[0])
                    r1datetime = parse(r[1])
                    r2float = float(r[2])
                    r3float = float(r[3])
                    if not r[4]:
                        raise ValueError("Field \"scientificName\" is empty.")
                except:
                    title = "Invalid Record Found"
                    content = "The following record is invalid and will be ignored:\n"
                    self.mainWindow.alert(title, content + pformat(r), 2)
                else:
                    self.spatialData[r[4]] = ((r2float, r3float), r0int)
                    self.temporalData[r[4]] = (r1datetime, r0int)
                    self.auxiliaryData[r[4]] = r[5]

            title = "Dataset Successfully Imported"
            content = "{:,d} records have been loaded.".format(len(dataList))
            self.mainWindow.alert(title, content, 0)

    # noinspection PyTypeChecker
    def setFilters(self):
        """
        Only leave filtered data in ``Dataset``.

        :return: None.
        """

        if not self.spatialData:
            title, content = "Empty Dataset", "Please import data first."
            self.mainWindow.alert(title, content, 3)

        else:
            xCoordinates = [n[0][1] for m in self.spatialData.values() for n in m]
            yCoordinates = [n[0][0] for m in self.spatialData.values() for n in m]
            timestamps = [n[0] for m in self.temporalData.values() for n in m]

            xCoordinateMinMax = (min(xCoordinates), max(xCoordinates))
            yCoordinateMinMax = (min(yCoordinates), max(yCoordinates))
            timestampMinMax = (min(timestamps), max(timestamps))

            dialog = SetFiltersDialog(xCoordinateMinMax, yCoordinateMinMax, timestampMinMax)
            dialog.exec_()

            if not dialog.xCoordinateMinMax:
                return

            for k in list(self.spatialData.keys()):
                for i, u in enumerate(self.spatialData[k]):
                    v = self.temporalData[k][i]
                    if (
                        dialog.xCoordinateMinMax[0] <= u[0][1] <= dialog.xCoordinateMinMax[1] and
                        dialog.yCoordinateMinMax[0] <= u[0][0] <= dialog.yCoordinateMinMax[1] and
                        dialog.timestampMinMax[0] <= v[0] <= dialog.timestampMinMax[1]
                    ):
                        break
                else:
                    if k in self.selectedSpecies:
                        self.removeSpecies(k + " " + self.auxiliaryData[k])
                    del self.spatialData[k]
                    del self.temporalData[k]
                    del self.auxiliaryData[k]
            self.cooccurrenceCalculation.halt()
            self.plot.resetCache()

            length = len([n for m in self.spatialData.values() for n in m])
            title = "Filter Result"
            content = "{:,d} records matches the specified range.".format(length)
            self.mainWindow.alert(title, content, 0)

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def addSpecies(self):
        """
        Select a species from ``Dataset.spatialData``, append it to ``Dataset.selectedSpecies``.

        :return: None.
        """

        if not self.spatialData:
            title, content = "Empty Dataset", "Please import data first."
            self.mainWindow.alert(title, content, 3)

        elif not Species.available():
            title = "Too Many Species"
            content = ("Selecting more than " + str(Species.nColor) +
                       " species is not supported.")
            self.mainWindow.alert(title, content, 3)

        else:
            species = [(k, self.auxiliaryData[k]) for k in self.spatialData.keys()
                       if k not in self.selectedSpecies]

            dialog = AddSpeciesDialog(species)
            dialog.exec_()

            if dialog.newSpecies:
                newSpecies, vernacularName = dialog.newSpecies

                self.selectedSpecies[newSpecies] = Species()
                newColor = self.selectedSpecies[newSpecies].color
                self.mainWindow.addSpeciesToLayout(newSpecies, vernacularName, newColor)
                self.map.add(newSpecies)
                self.map.refresh()
                self.plot.rebuild()
                self.correlationTable.add(newSpecies)

    def removeSpecies(self, oldSpecies):
        """
        Remove the specified species from ``Dataset.selectedSpecies``.

        :param oldSpecies: Name of the old species to be removed.
        :return: None.
        """

        oldSpeciesShort = oldSpecies
        for k in self.selectedSpecies.keys():
            if oldSpecies.startswith(k):
                oldSpeciesShort = k
                del self.selectedSpecies[k]
                break

        self.mainWindow.removeSpeciesFromLayout(oldSpecies)
        self.map.remove()
        self.map.refresh()
        self.plot.rebuild()
        self.correlationTable.remove(oldSpeciesShort)

    def clearData(self):
        """
        Clear ``Dataset``.

        :return: None.
        """

        if not self.spatialData:
            title, content = "Empty Dataset", "Please import data first."
            self.mainWindow.alert(title, content, 3)

        else:
            self.spatialData.clear()
            self.temporalData.clear()
            self.auxiliaryData.clear()
            self.selectedSpecies.clear()
            self.mainWindow.removeSpeciesFromLayout()
            self.map.rebuild()
            self.map.refresh()
            self.plot.resetCache()
            self.plot.rebuild()
            self.correlationTable.remove()
            self.cooccurrenceCalculation.halt()

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def about(self):
        """
        Show information about this program.

        :return: None.
        """

        title = "About Biodiversity Analysis"
        content = Dataset.license()
        self.mainWindow.alert(title, content, 4)
