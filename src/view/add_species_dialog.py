#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


# noinspection PyPep8Naming
class AddSpeciesDialog(QtWidgets.QDialog):

    # noinspection PyArgumentList, PyUnresolvedReferences
    def __init__(self, species):
        """
        Construct a dialog that allow the user to select a new species.

        :param species: List of distinct and unselected species in ``Dataset.dataset``.
        """

        super().__init__()
        self.newSpecies = ""

        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItems(species)

        label = QtWidgets.QLabel("&Select a species: ")
        label.setBuddy(self.comboBox)

        pushButton = QtWidgets.QPushButton("&Add")
        pushButton.setDefault(True)

        pushButton.clicked.connect(self.addSpeciesHandler)

        topLayout = QtWidgets.QHBoxLayout()
        topLayout.addWidget(label)
        topLayout.addWidget(self.comboBox)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(topLayout)
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

        self.newSpecies = self.comboBox.currentText()
        self.done(0)
