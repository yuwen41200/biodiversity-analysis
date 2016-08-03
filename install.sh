#!/bin/bash

python3.5 -m venv ba-env
source ba-env/bin/activate
pip install -r requirements.txt

# Workaround for `QWebEngine ICU not found` bug

cp -r ba-env/lib/python3.5/site-packages/PyQt5/Qt/resources/* \
    ba-env/lib/python3.5/site-packages/PyQt5/Qt/libexec/

mkdir -p ba-env/lib/python3.5/site-packages/PyQt5/Qt/libexec/qtwebengine_locales

cp -r ba-env/lib/python3.5/site-packages/PyQt5/Qt/resources/* \
    ba-env/lib/python3.5/site-packages/PyQt5/Qt/libexec/qtwebengine_locales/
