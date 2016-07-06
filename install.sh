#!/bin/bash

virtualenv -p /usr/bin/python3.5  --no-site-packages venv
. venv/bin/activate
pip install -r requirements.txt

# workaround of `QWebEngine ICU not found` bug
cp -r venv/lib/python3.5/site-packages/PyQt5/Qt/resources/ \
    venv/lib/python3.5/site-packages/PyQt5/Qt/libexec/

mkdir -p lib/python3.5/site-packages/PyQt5/Qt/libexec/qtwebengine_locales

cp -r venv/lib/python3.5/site-packages/PyQt5/Qt/resources/ \
    venv/lib/python3.5/site-packages/PyQt5/Qt/libexec/qtwebengine_locales
