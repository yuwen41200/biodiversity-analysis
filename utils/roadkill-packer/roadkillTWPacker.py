#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import Tk, messagebox, filedialog
from time import strftime
from os.path import basename
from string import Template
from zipfile import ZipFile

Tk().withdraw()
path = ''

while not path:
    messagebox.showinfo('', 'Please select the source file.')
    path = filedialog.askopenfilename()

with open('templates/eml.xml') as file:
    eml = file.read()

with open('templates/meta.xml') as file:
    meta = file.read()

data = {
    'eml_publication_date': strftime('%Y-%m-%d'),
    'meta_source_location': basename(path)
}

eml = Template(eml).substitute(data)
meta = Template(meta).substitute(data)

with ZipFile('dwca-roadkill-taiwan.zip', 'w') as zip_file:
    zip_file.writestr('eml.xml', eml)
    zip_file.writestr('meta.xml', meta)
    zip_file.write(path, basename(path))

messagebox.showinfo('', 'Successfully packed.')
