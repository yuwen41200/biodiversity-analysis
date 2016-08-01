#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


# noinspection PyPep8Naming
class AddSpeciesDialog(QtWidgets.QDialog):

    # noinspection PyArgumentList, PyUnresolvedReferences
    def __init__(self, species):
        """
        Construct a dialog that allows the user to select a new species.

        :param species: List of distinct and unselected species in ``Dataset.spatialData``.
        """

        super().__init__()
        self.species = [s[0] for s in species]
        self.newSpecies = ""

        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.header().hide()
        self.treeWidget.setSizePolicy(QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        ))
        self.treeWidget.setMinimumSize(600, 800)

        outerItems = {}
        for s in species:
            key = s[0][0].upper()
            if key in outerItems:
                outerItem = outerItems[key]
                innerItem1 = QtWidgets.QTreeWidgetItem(outerItem)
                innerItem1.setText(0, s[0])
                innerItem2 = QtWidgets.QTreeWidgetItem(outerItem)
                innerItem2.setText(1, s[1])
            else:
                outerItem = QtWidgets.QTreeWidgetItem()
                outerItem.setText(0, key)
                outerItems[key] = outerItem
                innerItem1 = QtWidgets.QTreeWidgetItem(outerItem)
                innerItem1.setText(0, s[0])
                innerItem2 = QtWidgets.QTreeWidgetItem(outerItem)
                innerItem2.setText(1, s[1])

        self.treeWidget.insertTopLevelItems(0, list(outerItems.values()))
        self.treeWidget.sortItems(0, Qt.AscendingOrder)

        label = QtWidgets.QLabel("&Select a species: ")
        label.setBuddy(self.treeWidget)

        pushButton = QtWidgets.QPushButton("&Add")
        pushButton.setDefault(True)

        self.treeWidget.itemDoubleClicked.connect(self.addSpeciesHandler)
        pushButton.clicked.connect(self.addSpeciesHandler)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(label)
        mainLayout.addWidget(self.treeWidget)
        mainLayout.addWidget(pushButton)
        mainLayout.setSizeConstraint(QtWidgets.QVBoxLayout.SetFixedSize)

        self.setWindowTitle("Add Species")
        self.setLayout(mainLayout)
        self.show()

    def addSpeciesHandler(self):
        """
        Handler function for the "Add" button.

        :return: None.
        """

        if (self.treeWidget.selectedItems() and
                self.treeWidget.selectedItems()[0].text(0) in self.species):
            self.newSpecies = self.treeWidget.selectedItems()[0].text(0)
            self.done(0)
