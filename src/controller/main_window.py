import os

from PyQt5 import QtWidgets

from model import datasetProcessor
from model.species import Species
from view import addSpeciesDialog


# noinspection PyPep8Naming, PyCallByClass, PyTypeChecker, PyArgumentList, PyBroadException
def importData(self):
    """
    Import data from a Darwin Core Archive (DwC-A). |br|
    Store them in MainWindow.dataset.

    :return: None.
    """

    title, extension = "Select a DwC-A File", "DwC-A File (*.zip)"
    filename = QtWidgets.QFileDialog.getOpenFileName(self, title, os.getcwd(), extension)[0]

    if filename:
        try:
            darwinCoreData = datasetProcessor.extractDarwinCoreArchive(filename)
            columns = ["decimalLatitude", "decimalLongitude", "scientificName"]
            dataList = datasetProcessor.extractCsv(darwinCoreData, columns)[1]
        except:
            title = "Invalid DwC-A File"
            content = (
                "The provided file is either not in DwC-A format or corrupted.\n"
                "Please select a valid one."
            )
            QtWidgets.QMessageBox.critical(self, title, content)
            return

        for r in dataList:
            self.dataset[r[2]] = (r[0], r[1])

        title = "Dataset Successfully Imported"
        content = "{:,d} records have been loaded.".format(len(dataList))
        QtWidgets.QMessageBox.information(self, title, content)


# noinspection PyPep8Naming, PyCallByClass, PyTypeChecker, PyArgumentList
def addSpecies(self):
    """
    Choose a species from the previous dataset. |br|
    Append it to MainWindow.selectedSpecies. |br|
    Then refresh the map.

    :return: None.
    """

    if not self.dataset:
        title, content = "Empty Dataset", "Please import data first."
        QtWidgets.QMessageBox.critical(self, title, content)

    elif not Species.available():
        title = "Too Many Species"
        content = "Selecting more than " + str(Species.nColor) + " species is not supported."
        QtWidgets.QMessageBox.critical(self, title, content)

    else:
        species = [k for k in self.dataset.keys() if k not in self.selectedSpecies]

        # noinspection PyPep8Naming, PyArgumentList
        def addSpeciesCallback(newSpecies):
            """
            Add the new species to MainWindow.speciesLayout.

            :param newSpecies: Name of the new species.
            :return: None.
            """

            self.selectedSpecies[newSpecies] = Species()
            self.map.addSpecies(self.dataset, newSpecies, self.selectedSpecies)

            label = QtWidgets.QLabel(newSpecies)
            label.setStyleSheet(
                "background-color: " + self.selectedSpecies[newSpecies].color + ";"
                "border-radius: 10px;"
                "padding-left: 10px;"
                "padding-right: 10px;"
            )
            label.setSizePolicy(QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
            ))
            self.speciesLayout.addWidget(label)

        dialog = addSpeciesDialog.AddSpeciesDialog(species, addSpeciesCallback)
        dialog.exec_()


# noinspection PyPep8Naming
def clearData(self):
    """
    Clear MainWindow.dataset and MainWindow.selectedSpecies. |br|
    Then refresh the map.

    :return: None.
    """

    self.dataset.clear()
    self.removeSpeciesFromLayout()
    self.map.refresh()


# noinspection PyPep8Naming
def removeSpeciesFromLayout(self, name=None):
    """
    Remove a species from the species layout. |br|
    If no species is given, it will remove all species.

    :param name: Name of species to be removed.
    :return: None.
    """

    if name:
        index = list(self.selectedSpecies.keys()).index(name)
        del self.selectedSpecies[name]
        indexes = [index]
    else:
        indexes = range(len(self.selectedSpecies))
        self.selectedSpecies.clear()

    for i in reversed(indexes):
        self.speciesLayout.itemAt(i).widget().setParent(None)


# noinspection PyCallByClass, PyTypeChecker, PyArgumentList
def about(self):
    """
    Show information about this program.

    :return: None.
    """

    title = "About Biodiversity Analysis"
    content = (
        "<h1>Biodiversity Analysis</h1>"
        "<p><b>Biodiversity Data Analysis and Visualization</b><br>"
        "Copyright (C) 2016 Yu-wen Pwu and Yun-chih Chen<br>"
        "<a href='https://github.com/yuwen41200/biodiversity-analysis'>"
        "https://github.com/yuwen41200/biodiversity-analysis</a></p>"
        "<p>This program is free software: you can redistribute it and/or modify "
        "it under the terms of the GNU General Public License as published by "
        "the Free Software Foundation, either version 3 of the License, or "
        "(at your option) any later version.</p>"
        "<p>This program is distributed in the hope that it will be useful, "
        "but WITHOUT ANY WARRANTY; without even the implied warranty of "
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the "
        "GNU General Public License for more details.</p>"
        "<p>You should have received a copy of the GNU General Public License "
        "along with this program. If not, see <a href='http://www.gnu.org/licenses/'>"
        "http://www.gnu.org/licenses/</a>.</p>"
        "<p>&nbsp;</p>"
    )
    QtWidgets.QMessageBox.about(self, title, content)
