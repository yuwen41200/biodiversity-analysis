#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from zipfile import ZipFile
from random import sample
from fnmatch import fnmatch
from functools import reduce
from xml.dom import minidom
from codecs import unicode_escape_decode


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
        """
        Retrieve the value of an attribute in a DOM.

        :param dom: DOM object.
        :param attribute: Attribute name.
        :param default: If ``attribute`` is not found in ``dom``, apply this value.
        :return: Value of ``attribute`` in ``dom``.
        """

        return (unicode_escape_decode(dom.attributes[attribute].value)[0]
                if attribute in dom.attributes.keys() else default)

    @staticmethod
    def extractDarwinCoreField(core):
        """
        Extract fields of a given core.

        :param core: DOM object of the core.
        :return: Fields of the given core, sorted by index.
        """

        idDom = core.getElementsByTagName("id")
        doms = core.getElementsByTagName("field")
        indexes = [int(DatasetProcessor.getXmlAttribute(dom, "index", default=-1)) for dom in doms]
        indexes = filter(lambda t: t >= 0, indexes)
        fields = [DatasetProcessor.getXmlAttribute(dom, "term").split("/")[-1] for dom in doms]
        sortedFields = sorted(zip(indexes, fields), key=lambda field: field[0])

        idIndex = int(DatasetProcessor.getXmlAttribute(idDom[0], "index", "0")) if idDom else 0
        fields = list(map(lambda field: field[1], sortedFields))
        fields.insert(idIndex, "id")

        return fields

    @staticmethod
    def extractDarwinCoreType(rowType):
        """
        Determine the type of the core, given rowType URI. |br|
        See http://tdwg.github.io/dwc/terms/guides/text/#coreTag for all available types.

        :param rowType: The rowType URI.
        :return: The type of the core.
        """

        return rowType.split("/")[-1]

    @staticmethod
    def extractDarwinCoreArchive(filename):
        """
        Extract data from a Darwin Core Archive (DwC-A) file.

        :param filename: The name of the Darwin Core Archive (DwC-A) file.
        :return: Extracted data and metadata, in tuple.
        """

        with ZipFile(filename) as zipped:
            meta = DatasetProcessor.readFileFromZip(zipped, "meta.xml")

            # Get the name of the data file by parsing ``meta.xml``.
            xml = minidom.parseString(meta)
            core = xml.getElementsByTagName("core")[0]
            metaDefaults = {
                "encoding": "utf-8",
                "fieldsTerminatedBy": ",",
                "linesTerminatedBy": "\n",
                "rowType": "http://rs.tdwg.org/dwc/xsd/simpledarwincore/SimpleDarwinRecord",
                "ignoreHeaderLines": "1"
            }
            metadata = {key: DatasetProcessor.getXmlAttribute(core, key, default=default)
                        for key, default in metaDefaults.items()}

            metadata["fields"] = DatasetProcessor.extractDarwinCoreField(core)
            metadata["coreType"] = DatasetProcessor.extractDarwinCoreType(metadata["rowType"])
            metadata["ignoreHeaderLines"] = bool(metadata["ignoreHeaderLines"])
            dataFilename = core.getElementsByTagName("location")[0].firstChild.data

            return (DatasetProcessor.readFileFromZip(zipped, dataFilename)
                    .decode(encoding=metadata["encoding"]), metadata)

    @staticmethod
    def extractCsv(csvStr, metadata, selectedFields=None):
        """
        Select data from a CSV-formatted string.

        :param csvStr: The string representing the CSV data.
        :param metadata: The metadata of this CSV data.
        :param selectedFields: The list of selected fields.
        :return: The list of records. |br|
                 Each record is a list containing only the selected fields.
        """

        if selectedFields is None:
            selectedFields = []

        fields = metadata["fields"]
        delimiter = metadata["fieldsTerminatedBy"]
        lines = csvStr.split(metadata["linesTerminatedBy"])
        startLine = 1 if metadata["ignoreHeaderLines"] else 0

        if selectedFields:
            selectedIndices = []
            for field in selectedFields:
                name, required = field
                if name not in fields:
                    if required:
                        raise ValueError("Required field \"" + name + "\" not found.")
                    selectedIndices.append(-1)
                else:
                    selectedIndices.append(fields.index(name))

            data = []
            for line in lines[startLine:]:
                if line:
                    _line = line.split(delimiter)
                    data.append([_line[i] if i >= 0 else "" for i in selectedIndices])

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
        coordSum = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), randomDraws)
        return coordSum[0] / draw, coordSum[1] / draw
