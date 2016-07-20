#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from model.dataset import Dataset
from model.species import Species
from view.add_species_dialog import AddSpeciesDialog
from controller.leaflet_map import LeafletMap
from lib.dataset_processor import DatasetProcessor


class MainAction:

    # noinspection PyPep8Naming
    def __init__(self, dataset: Dataset, mainWindow) -> None:
        self.dataset = dataset.dataset
        self.selectedSpecies = dataset.selectedSpecies

        self.mainWindow = mainWindow
        self.mainWindow.setupWidgets(self, LeafletMap())
        self.mainWindow.show()

    # noinspection PyPep8Naming, PyCallByClass, PyTypeChecker, PyArgumentList, PyBroadException
    def importData(self) -> None:
        """
        Import data from a Darwin Core Archive (DwC-A). |br|
        Store them in Dataset.dataset.

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

    # noinspection PyPep8Naming, PyCallByClass, PyTypeChecker, PyArgumentList
    def addSpecies(self) -> None:
        """
        Choose a species from the previous dataset. |br|
        Append it to MainWindow.selectedSpecies. |br|
        Then refresh the map.

        :return: None.
        """

        if not self.dataset:
            title, content = "Empty Dataset", "Please import data first."
            self.mainWindow.alert(title, content, 3)

        elif not Species.available():
            title = "Too Many Species"
            content = "Selecting more than " + str(Species.nColor) + " species is not supported."
            self.mainWindow.alert(title, content, 3)

        else:
            species = [k for k in self.dataset.keys() if k not in self.selectedSpecies]

            dialog = AddSpeciesDialog(species)
            dialog.exec_()

            newSpecies = dialog.newSpecies
            self.selectedSpecies[newSpecies] = Species()
            self.mainWindow.addSpeciesToLayout(self.dataset, newSpecies, self.selectedSpecies)

    # noinspection PyPep8Naming
    def clearData(self) -> None:
        """
        Clear MainWindow.dataset and MainWindow.selectedSpecies. |br|
        Then refresh the map.

        :return: None.
        """

        indices = range(len(self.selectedSpecies))
        self.mainWindow.removeSpeciesFromLayout(indices)

        self.dataset.clear()
        self.selectedSpecies.clear()

    # noinspection PyCallByClass, PyTypeChecker, PyArgumentList
    def about(self) -> None:
        """
        Show information about this program.

        :return: None.
        """

        title = "About Biodiversity Analysis"
        content = Dataset.license()
        self.mainWindow.alert(title, content, 4)
