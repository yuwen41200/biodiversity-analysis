#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile
import fnmatch
import re
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

        # TODO: extract field name from data file
        data = readFileFromZIP(zipF, dataFilename)
