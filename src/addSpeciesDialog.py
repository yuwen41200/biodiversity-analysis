#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout


# noinspection PyPep8Naming
class AddSpeciesDialog(QDialog):

    # noinspection PyArgumentList
    def __init__(self, species, selectedSpecies):
        """
        Construct the dialog, given a list of species.

        :param species: List of distinct species in the dataset.
        :param selectedSpecies: List of already selected species.
                                This list will be modified.
        """

        super().__init__()
        self.selectedSpecies = selectedSpecies

        self.comboBox = QComboBox()
        self.comboBox.addItems(species)

        label = QLabel("Select a species: ")
        label.setBuddy(self.comboBox)

        pushButton = QPushButton("Add")
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
        Append the chosen species to AddSpeciesDialog.selectedSpecies.

        :return: None.
        """

        item = self.comboBox.currentText()
        self.selectedSpecies.append(item)
        self.done(0)
