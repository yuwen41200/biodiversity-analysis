#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from window import MainWindow
from leafletMap import Map

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    leafletMap = Map()
    window = MainWindow(leafletMap)
    window.show()
    sys.exit(app.exec_())
