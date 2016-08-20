#!/bin/bash

python3.5 -m venv ba-env --system-site-packages
source ba-env/bin/activate
pip3.5 install --upgrade pip
pip3.5 install -I -r requirements.txt

# Workaround for `QWebEngine ICU not found` bug

cp -rn ba-env/lib/python3.5/site-packages/PyQt5/Qt/resources/* \
    ba-env/lib/python3.5/site-packages/PyQt5/Qt/libexec/

mkdir -p ba-env/lib/python3.5/site-packages/PyQt5/Qt/libexec/qtwebengine_locales

cp -rn ba-env/lib/python3.5/site-packages/PyQt5/Qt/resources/* \
    ba-env/lib/python3.5/site-packages/PyQt5/Qt/libexec/qtwebengine_locales/
