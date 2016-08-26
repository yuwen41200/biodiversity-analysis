#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import Tk, messagebox, filedialog
from sys import exit, argv
from os import path
from logging import basicConfig, DEBUG, debug
from time import strftime
from string import Template
from zipfile import ZipFile

import htmlGenerator

Tk().withdraw()
messagebox.showinfo('Roadkill Packer', 'Please select the source file.')
src_path = filedialog.askopenfilename()

if not src_path:
    exit(1)

eml_path = path.join(path.dirname(path.realpath(__file__)), 'templates', 'eml.xml')
meta_path = path.join(path.dirname(path.realpath(__file__)), 'templates', 'meta.xml')
browse_path = path.join(path.dirname(path.realpath(__file__)), 'browse.html')

if len(argv) > 1 and argv[1] == 'DEBUG':
    basicConfig(level=DEBUG)

debug('eml.xml at ' + eml_path)
debug('meta.xml at ' + meta_path)
debug('source file at ' + src_path)
debug('browse.html at ' + browse_path)

with open(eml_path) as file:
    eml = file.read()

with open(meta_path) as file:
    meta = file.read()

data = {
    'eml_publication_date': strftime('%Y-%m-%d'),
    'meta_source_location': path.basename(src_path)
}

eml = Template(eml).substitute(data)
meta = Template(meta).substitute(data)
htmlGenerator.generate(src_path, browse_path)

with ZipFile('dwca-roadkill-taiwan.zip', 'w') as zip_file:
    zip_file.writestr('eml.xml', eml)
    zip_file.writestr('meta.xml', meta)
    zip_file.write(src_path, path.basename(src_path))
    zip_file.write(browse_path, 'browse.html')

messagebox.showinfo('Roadkill Packer', 'Successfully packed.')
