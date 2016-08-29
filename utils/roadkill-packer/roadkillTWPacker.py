#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import Tk, messagebox, filedialog
from sys import exit, argv
from os import path, walk
from logging import basicConfig, DEBUG, debug
from time import strftime
from string import Template
from subprocess import run
from zipfile import ZipFile, ZIP_DEFLATED

import htmlGenerator

Tk().withdraw()
messagebox.showinfo('Roadkill Packer', 'Please select the source file.')
src_path = filedialog.askopenfilename()

if not src_path:
    exit(1)

eml_path = path.join(path.dirname(path.realpath(__file__)), 'templates', 'eml.xml')
meta_path = path.join(path.dirname(path.realpath(__file__)), 'templates', 'meta.xml')
src_tmp_path = path.join(path.dirname(path.realpath(__file__)), path.basename(src_path) + '.tmp')
browse_path = path.join(path.dirname(path.realpath(__file__)), 'browse.html')
trans_path = path.join(path.dirname(path.realpath(__file__)), 'roadkillTransformer.sh')
photo_path = path.join(path.dirname(path.realpath(__file__)), 'roadkill-photo')

if len(argv) > 1 and argv[1] == 'DEBUG':
    basicConfig(level=DEBUG)

debug('eml.xml at ' + eml_path)
debug('meta.xml at ' + meta_path)
debug('source file at ' + src_path)
debug('source temporary file at ' + src_tmp_path)
debug('browse.html at ' + browse_path)
debug('roadkillTransformer.sh at ' + trans_path)
debug('roadkill-photo at ' + photo_path)

with open(eml_path) as file:
    eml = file.read()

with open(meta_path) as file:
    meta = file.read()

with open(src_path) as file:
    with open(src_tmp_path, 'w') as file_tmp:
        is_first_line = True
        for line in file:
            line = line.strip()
            if is_first_line:
                file_tmp.write(line + ',photo\n')
                is_first_line = False
            else:
                file_tmp.write(line + ',roadkill-photo/' + line.split(',', 1)[0] + '.jpg\n')

data = {
    'eml_publication_date': strftime('%Y-%m-%d'),
    'meta_source_location': path.basename(src_path)
}

eml = Template(eml).substitute(data)
meta = Template(meta).substitute(data)
htmlGenerator.generate(src_tmp_path, browse_path)
run([trans_path, '-i', src_path, '-d', photo_path], check=True)

with ZipFile('dwca-roadkill-taiwan.zip', 'w', ZIP_DEFLATED) as zip_file:
    zip_file.writestr('eml.xml', eml)
    zip_file.writestr('meta.xml', meta)
    zip_file.write(src_tmp_path, path.basename(src_path))
    zip_file.write(browse_path, 'browse.html')
    for dirpath, dirnames, filenames in walk(photo_path):
        for filename in filenames:
            zip_file.write(path.join(dirpath, filename), path.join('roadkill-photo', filename))

messagebox.showinfo('Roadkill Packer', 'Successfully packed.')
