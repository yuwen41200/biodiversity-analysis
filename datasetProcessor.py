#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile, fnmatch, re, csv
import xml.etree.ElementTree as xmlParser

def readFileFromZIP(zipHandle, basename):
    # Get full filename from Zip handle
    fullFilename = next(f for f in zipHandle.namelist() if fnmatch.fnmatch(f, '*' + basename))
    return zipHandle.read(fullFilename)

def extractDarwinCoreArchive(fileName):
    with zipfile.ZipFile(fileName) as zipF:
        meta = readFileFromZIP(zipF, "meta.xml")

        ###
        ### Get full filename of data file by parsing meta.xml
        ###
        xml = xmlParser.fromstring(meta)
        xmlNamespace = xml.tag.split("archive")[0]
        dataFilename = xml.find(".//" + xmlNamespace + "location").text

        return readFileFromZIP(zipF, dataFilename).decode(encoding="utf-8")

def extractCsv(csvStr, selectedFields=[]):
    lines = csvStr.split('\n')
    delim = ',' if ',' in lines[0] else '\t'
    fields = lines[0].split(delim)

    selectedFields = filter(lambda f: f in fields, selectedFields)
    if selectedFields:
        data = []
        selectedIndexes = map(lambda f: fields.index(f), selectedFields)
        for line in lines[1:]:
            _line = line.split(delim)
            data.append([_line[i] for i in selectedIndexes])
    else:
        data = [line.split(delim) for line in lines[1:]]

    return (fields, data)
