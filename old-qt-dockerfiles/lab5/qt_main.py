#!/usr/bin/env python3
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtCore import *

import sys
import resource_rc

if __name__ == '__main__':
	app = QApplication(sys.argv)
	engine = QQmlApplicationEngine()
	engine.load(QUrl('pycam.qml'))
	app.exec_()
	#sys.exit(app.exec_())
	while True: 
		pass


