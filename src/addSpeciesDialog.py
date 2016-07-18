#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QPushButton, QHBoxLayout, \
                            QVBoxLayout, QSizePolicy
from species import Species


# noinspection PyPep8Naming
class AddSpeciesDialog(QDialog):

    # noinspection PyArgumentList
    def __init__(self, species, selectedSpecies, speciesLayout):
        """
        Construct the dialog, given a list of species.

        :param species: List of distinct species in the dataset.
        :param selectedSpecies: Dictionary of already selected species.
                                This dictionary will be modified.
        :param speciesLayout: A layout which lists all selected species.
                              This layout will be modified.
        """

        super().__init__()
        self.selectedSpecies = selectedSpecies
        self.speciesLayout = speciesLayout

        self.comboBox = QComboBox()
        self.comboBox.addItems(species)

        label = QLabel("&Select a species: ")
        label.setBuddy(self.comboBox)

        pushButton = QPushButton("&Add")
        pushButton.setDefault(True)

        # noinspection PyUnresolvedReferences
        pushButton.clicked.connect(self.addSpeciesHandle)

        topLayout = QHBoxLayout()
        topLayout.addWidget(label)
        topLayout.addWidget(self.comboBox)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(pushButton)
        mainLayout.setSizeConstraint(QVBoxLayout.SetFixedSize)

        self.setWindowTitle("Add Species")
        self.setLayout(mainLayout)
        self.show()

    def addSpeciesHandle(self):
        """
        Add the chosen species to AddSpeciesDialog.selectedSpecies.
        Also append it to AddSpeciesDialog.speciesLayout.

        :return: None.
        """

        item = self.comboBox.currentText()
        self.selectedSpecies[item] = Species()

        label = QLabel(item)
        label.setStyleSheet(
            "background-color: " + self.selectedSpecies[item].color + ";"
            "border-radius: 10px;"
            "padding-left: 10px;"
            "padding-right: 10px;"
        )
        label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.speciesLayout.addWidget(label)

        self.done(0)
