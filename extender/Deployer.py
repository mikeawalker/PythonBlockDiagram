import base.Extender as Extend
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Deployer:
    def __init__(self):
        pass
    def create(self):
        pass
    def validate(self):
        pass
class DeployerExtender(Extend.Extender):
    """description of class"""
    def __init__(self ):
        super().__init__("Deployer" )
        self.deployer = Deployer()
    def TranslateToDiagram( self , dataTree ):
        pass
    def TranslateToData( self , diagramTree ):
        pass
    # ------ Block Right Click --------- #
    def BlockRightClick( self  , menu):
        hw = menu.addAction('Hardware Info')
        hw.triggered.connect(self.HwDisplay)
    # ------- Port right click ----------#
    def PortRightClick( self ):
        print("Extra Port Right Click")
    ##### meenu extender
    def ExtraMenuItems( self  , menuBar ):
      # make an about box
      help = menuBar.addMenu('Help')
      about = QAction('About', self.editor)        
      about.triggered.connect( self.AboutBox)  
      help.addAction(about)
      # make the Deployment menu
      deploy = menuBar.addMenu('Deploy')
      validate = QAction('Validate Design', self.editor)        
      validate.triggered.connect( self.deployer.validate)  
      deploy.addAction(validate)
      create = QAction('Create Design' , self.editor)
      create.triggered.connect( self.deployer.create)  #LoadLib
      deploy.addAction(create)
    # ---- Non Inherited stuffz ---- #
    def AboutBox(self):
        print("AboutBox")
    def HwDisplay(self):
      pd = HardwareDialog(self.editor.window())
      pd.exec_()
class HardwareDialog(QDialog):
   def __init__(self, parent=None):
      super(HardwareDialog, self).__init__(parent)
      self.button = QPushButton('Done', self)
      l = QVBoxLayout(self)
      l.addWidget(self.button)
      self.button.clicked.connect(self.OK)
   def OK(self):
      self.close()