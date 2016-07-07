#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile

def extractDarwinCoreArchive(filename):
    with zipfile.ZipFile(zipF, 'r') as zipF:
        meta = zipF.open("meta.xml")
        # TODO
        # Open other files in the archive here

    zipF.close()
