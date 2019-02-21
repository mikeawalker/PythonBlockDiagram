from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import xml.etree.ElementTree as ET

#class PortItem(QGraphicsEllipseItem  ):
class PortItem(QGraphicsRectItem  ):
   """ Represents a port to a subsystem """
   def __init__(self, name, dir,  parent=None):

      QGraphicsRectItem.__init__(self, -5,-10,10.0,20.0, parent)
      self.block = parent
      self.setCursor(QCursor(Qt.CrossCursor))
      self.editor = parent.editor
      self.colorDict  = dict()
      self.colorDict["In"] = Qt.green
      self.colorDict["Out"] = Qt.green
      self.colorDict["TwoWay"] = Qt.blue
      # Properties:
      self.setBrush(QBrush(self.colorDict[dir]))
      # Name:
      self.name = name
      self.direction = dir
      
      self.posCallbacks = []
      self.connection = None
      self.setFlag(self.ItemSendsScenePositionChanges, True)
   def itemChange(self, change, value):
      if change == self.ItemScenePositionHasChanged:
         for cb in self.posCallbacks:
            cb(value)
         return value
      return super(PortItem, self).itemChange(change, value)
   def getDirection( self ):
       return self.direction
   def connect( self , connection ):
       self.connection = connection
   def disconnect( self ):
       if( self.connection is not None ):
           self.connection.delete( )
   def removeConnection(self  ):
       self.connection = None
   def GetName(self):
       return  self.block.name + "/" + self.name
   def mousePressEvent(self, event):
      if event.button() == Qt.LeftButton:
        self.connection = self.editor.startConnection(self)
      elif event.button() == Qt.RightButton:
        self.ClickMenu( event )
   def DisplayPortInfo( self ):
       print("POrt info")
   def ClickMenu( self ,event ):
      menu = QMenu()
      dc = menu.addAction('Disconnect')
      inf = menu.addAction('Info')
      dc.triggered.connect(self.disconnect)
      inf.triggered.connect( self.DisplayPortInfo )
      #self.extender.

      menu.exec_(event.screenPos())
class PortParams( QDialog) :
   def __init__(self, parent=None):
      super(ParameterDialog, self).__init__(parent)
      self.button = QPushButton('Ok', self)
      l = QVBoxLayout(self)
      l.addWidget(self.button)
      self.button.clicked.connect(self.OK)
   def OK(self):
      self.close()
