#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
from leafletMap import LeafletMap

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow(LeafletMap())
    window.show()
    sys.exit(app.exec_())
