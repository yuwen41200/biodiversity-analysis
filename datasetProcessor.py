#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile
import fnmatch
import xml.etree.ElementTree as xmlParser


# noinspection PyPep8Naming
def readFileFromZip(zipHandle, basename):
    """
    Get full filename from a ZIP handle, then extract the file.
    :param zipHandle: The ZIP handle.
    :param basename: The base of the full filename.
    :return: The extracted data.
    """
    fullFilename = next(f for f in zipHandle.namelist() if fnmatch.fnmatch(f, '*' + basename))
    return zipHandle.read(fullFilename)


# noinspection PyPep8Naming
def extractDarwinCoreArchive(filename):
    """
    Extract data from a Darwin Core Archive (DwC-A).
    :param filename: The name of the Darwin Core Archive (DwC-A).
    :return: The extracted data.
    """
    with zipfile.ZipFile(filename) as zipped:
        meta = readFileFromZip(zipped, "meta.xml")

        # Get the name of the data file by parsing meta.xml
        xml = xmlParser.fromstring(meta)
        xmlNamespace = xml.tag.split("archive")[0]
        dataFilename = xml.find(".//" + xmlNamespace + "location").text

        return readFileFromZip(zipped, dataFilename).decode(encoding="utf-8")


# noinspection PyPep8Naming
def extractCsv(csvStr, selectedFields=None):
    """
    Select data from a CSV-formatted string.
    :param csvStr: The string representing the CSV data.
    :param selectedFields: The list of selected fields.
    :return: The list of records, each record is a list containing only the selected fields.
    """
    if selectedFields is None:
        selectedFields = []

    lines = csvStr.split('\n')
    delimiter = ',' if ',' in lines[0] else '\t'
    fields = lines[0].split(delimiter)

    selectedFields = list(filter(lambda f: f in fields, selectedFields))
    if selectedFields:
        selectedIndices = []
        for field in selectedFields:
            selectedIndices.append(fields.index(field))

        data = []
        for line in lines[1:]:
            if line:
                _line = line.split(delimiter)
                data.append([_line[i] for i in selectedIndices])
    else:
        # Default: select all fields
        selectedIndices = range(len(fields))
        data = [line.split(delimiter) for line in lines[1:]]

    return selectedIndices, data
