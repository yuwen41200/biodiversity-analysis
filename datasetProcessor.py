#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile, fnmatch, re, csv
import xml.etree.ElementTree as xmlParser


# noinspection PyPep8Naming
def readFileFromZIP(zipHandle, basename):
    """ Get full filename from Zip handle """
    fullFilename = next(f for f in zipHandle.namelist() if fnmatch.fnmatch(f, '*' + basename))
    return zipHandle.read(fullFilename)


# noinspection PyPep8Naming
def extractDarwinCoreArchive(fileName):
    with zipfile.ZipFile(fileName) as zipF:
        meta = readFileFromZIP(zipF, "meta.xml")

        # Get full filename of data file by parsing meta.xml
        xml = xmlParser.fromstring(meta)
        xmlNamespace = xml.tag.split("archive")[0]
        dataFilename = xml.find(".//" + xmlNamespace + "location").text

        return readFileFromZIP(zipF, dataFilename).decode(encoding="utf-8")


# noinspection PyPep8Naming
def extractCsv(csvStr, selectedFields=[]):
    lines = csvStr.split('\n')
    delimiter = ',' if ',' in lines[0] else '\t'
    fields = lines[0].split(delimiter)

    if len(lines) <= 1:
        raise Exception("Empty csv given")
        return ([],[])

    selectedFields = list(filter(lambda f: f in fields, selectedFields))
    if selectedFields:
        selectedIndexes = []
        for field in selectedFields:
            if field in fields:
                selectedIndexes.append(fields.index(field))
            else:
                raise Exception("field `%s` is in the dataset" % field)

        data = []
        for line in lines[1:]:
            if line:
                _line = line.split(delim)
                data.append([_line[i] for i in selectedIndexes])
    else:
        # Default: select all fields
        selectedIndexes = range(len(fields))
        data = [line.split(delim) for line in lines[1:]]

    return (selectedIndexes, data)
