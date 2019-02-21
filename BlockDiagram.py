#import os
#import sys
#from PyQt5.QtWidgets import *
#from DragNDrop import *
#from BlockApp import *

#!/usr/bin/python

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from base.Port import PortItem
from base.Connection import Connection
from base.Block import BlockItem
from base.DiagramEditor import *
from extender.Deployer import *




if __name__ == '__main__':
   app = QApplication(sys.argv)
   deployer = DeployerExtender()
   editor = DiagramEditor( deployer )
   editor.show()
   editor.resize(700, 800)
   app.exec_()