from PyQt4.QtGui import *
from PyQt4.QtCore import *

from MainUI import *

import sys

def main():

	app = QtGui.QApplication(sys.argv)
	mainWidget = MainUI()
	sys.exit(app.exec_())


if __name__ == '__main__':
    main()
