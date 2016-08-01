#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from zipfile import ZipFile
from random import sample
from fnmatch import fnmatch
from functools import reduce
from xml.dom import minidom as dom
from codecs import unicode_escape_decode as escape

# noinspection PyPep8Naming
class DatasetProcessor:

    @staticmethod
    def readFileFromZip(zipHandle, basename):
        """
        Get full filename from a ZIP handle, then extract the file.

        :param zipHandle: The ZIP handle.
        :param basename: The base of the full filename.
        :return: The extracted data.
        """

        fullFilename = next(f for f in zipHandle.namelist() if fnmatch(f, '*' + basename))
        return zipHandle.read(fullFilename)

    @staticmethod
    def getXmlAttribute(dom, attribute, default=None):
        return escape(dom.attributes[attribute].value)[0] if attribute in dom.attributes.keys() else default

    @staticmethod
    def extractDarwinCoreArchive(filename):
        """
        Extract data from a Darwin Core Archive (DwC-A) file.

        :param filename: The name of the Darwin Core Archive (DwC-A) file.
        :return: Extracted data and extracted meta data, in tuple
        """

        with ZipFile(filename) as zipped:
            meta = DatasetProcessor.readFileFromZip(zipped, "meta.xml")

            # Get the name of the data file by parsing ``meta.xml``.
            xml = dom.parseString(meta)
            core = xml.getElementsByTagName("core")[0]
            metaDefaults = {
                "encoding": "utf-8",
                "fieldsTerminatedBy": ",",
                "linesTerminatedBy": "\n",
                "rowType": "http://rs.tdwg.org/dwc/xsd/simpledarwincore/SimpleDarwinRecord",
                "ignoreHeaderLines": "1"
            }
            metaData = {key: DatasetProcessor.getXmlAttribute(core, key, default=default) for key,default in metaDefaults.items()}

            metaData["coreType"] = DatasetProcessor.extractDarwinCoreType(metaData["rowType"])
            metaData["ignoreHeaderLines"] = bool(metaData["ignoreHeaderLines"])
            dataFilename = core.getElementsByTagName("location")[0].firstChild.data

            return (DatasetProcessor.readFileFromZip(zipped, dataFilename)
                    .decode(encoding=metaData["encoding"]), metaData)

    @staticmethod
    def extractDarwinCoreType(rowType):
        """
        Determine the type of core, given rowType URI
        see "http://tdwg.github.io/dwc/terms/guides/text/#coreTag" for all available types

        :param rowType: the rowType URI
        :return: The type of core
        """
        return rowType.split("/")[-1]

    @staticmethod
    def extractCsv(csvStr, meta, selectedFields=[]):
        """
        Select data from a CSV-formatted string.

        :param csvStr: The string representing the CSV data.
        :param meta: The meta data of this csv
        :param selectedFields: The list of selected fields.
        :return: The list of records. |br|
                 Each record is a list containing only the selected fields.
        """

        delimiter = meta["fieldsTerminatedBy"]
        lines = csvStr.split(meta["linesTerminatedBy"])
        fields = lines[0].split(delimiter)
        startLine = 1 if meta["ignoreHeaderLines"] else 0

        selectedFields = list(filter(lambda f: f in fields, selectedFields))

        if selectedFields:
            selectedIndices = []
            for field in selectedFields:
                selectedIndices.append(fields.index(field))

            data = []
            for line in lines[startLine:]:
                if line:
                    _line = line.split(delimiter)
                    data.append([_line[i] for i in selectedIndices])

        else:
            # Default: select all fields.
            data = [line.split(delimiter) for line in lines[startLine:]]

        return data

    @staticmethod
    def randomEstimateLocation(coordinates):
        """
        Estimate the center coordinate by averaging 10% of all coordinates.

        :param coordinates: The list of coordinates, in tuple.
        :return: The center coordinate, in tuple.
        """

        dataNum = len(coordinates)
        assert(dataNum and len(coordinates[0]) == 2)

        draw = int(dataNum * 0.1)
        if not draw:
            draw = dataNum

        randomDraws = sample(coordinates, draw)

        # Ensure they are floats, not strings.
        for idx, val in enumerate(randomDraws):
            randomDraws[idx] = (float(val[0]), float(val[1]))

        coordSum = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), randomDraws)
        return coordSum[0] / draw, coordSum[1] / draw
