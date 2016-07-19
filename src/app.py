#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
from leafletMap import LeafletMap

if __name__ == '__main__':
    # QTBUG-49940 workaround
    os.environ["LIBOVERLAY_SCROLLBAR"] = "0"
    app = QApplication(sys.argv)
    window = MainWindow(LeafletMap())
    window.show()
    sys.exit(app.exec_())
