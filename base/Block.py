import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pathlib import Path

from base.Port import *
class BlockItem(QGraphicsRectItem):
   """ 
      Represents a block in the diagram
      Has an x and y and width and height
      width and height can only be adjusted with a tip in the lower right corner.

      - in and output ports
      - parameters
      - description
   """
   def __init__(self, tre ,editor, parent=None):
      super(BlockItem, self).__init__(parent)
      w = 60.0
      h = 40.0
      name = tre.get("Name")
      self.name = name 
      self.BlockTree = tre

      self.editor = editor
      # Properties of the rectangle:
      self.setPen(QPen(Qt.blue, 2))
      self.setBrush(QBrush(Qt.lightGray))
      self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
      self.setCursor(QCursor(Qt.PointingHandCursor))
      # Label:
      self.label = QGraphicsTextItem(name , self)
      # Create corner for resize:
      self.sizer = HandleItem(self)
      self.sizer.setPos(w, h)
      self.sizer.posChangeCallbacks.append(self.changeSize) # Connect the callback
      #self.sizer.setVisible(False)
      self.sizer.setFlag(self.sizer.ItemIsSelectable, True)

      # Inputs and outputs of the block:
      self.inputs = dict() #[]
      self.outputs = dict() #[]
      self.multis = dict() #[]
      for item in self.BlockTree.findall("Port"):
        self.AddPort( item )

      # Update size:
      self.changeSize(w, h)

   
   def CreateOutput( self  ):
      self.OutTree = ET.Element("Block")
      n = ET.SubElement( self.OutTree , "Name")
      t = ET.SubElement( self.OutTree , "Type")
      l = ET.SubElement( self.OutTree , "Library")
      n.text = self.BlockTree.get("Name")
      l.text = self.BlockTree.find("Library").text
      t.text = self.BlockTree.find("Type").text
      self.OutTree.set("DX", str(self.w))
      self.OutTree.set("DY",  str(self.h))
      self.OutTree.set("X",str(self.x()) )
      self.OutTree.set("Y", str(self.y()))
   def CleanupPorts( self ):
        for port in self.inputs.values():
            port.disconnect()
        for port in self.outputs.values():
            port.disconnect()
        for port in self.multis.values():
            port.disconnect()
   def Delete( self ):
       self.CleanupPorts()
       self.editor.diagramScene.RemoveBlock( self.BlockTree.get("Name") )
   def GetPort( self , name ):
       if name in self.inputs:
           return self.inputs[name]
       if name in self.outputs:
           return self.outputs[name]
       if name in self.multis:
           return self.multis[name]
   def AddPort(self , portTree  ):
       direction = portTree.get("Direction")
       portname = portTree.get("Name")
       if( direction == "In" ):
           self.inputs[portname] =  PortItem( portname , "In" ,self )
       elif(direction == "Out" ):
           self.outputs[portname] =   PortItem( portname , "Out" ,self )
       else:
           self.inputs[portname] =   PortItem( portname , "TwoWay" , self)
       port = ET.SubElement( self.BlockTree , 'Port')
       
       

   def editParameters(self):
      pd = ParameterDialog(self.window())
      pd.exec_()

   def contextMenuEvent(self, event):
      menu = QMenu()
      delete = menu.addAction('Delete')
      pa = menu.addAction('Parameters')
      pa.triggered.connect(self.editParameters)
      delete.triggered.connect( self.Delete )
      
      self.editor.extender.BlockRightClick( menu )
      
      menu.exec_(event.screenPos())

   def getTree( self ):
       self.CreateOutput()
       return self.OutTree

   def changeSize(self, w, h):
      """ Resize block function """
      # Limit the block size:
      if h < 20:
         h = 20
      if w < 40:
         w = 40
      self.setRect(0.0, 0.0, w, h)
      # center label:
      rect = self.label.boundingRect()
      lw, lh = rect.width(), rect.height()
      lx = (w - lw) / 2
      ly = (h - lh) / 2
      self.label.setPos(lx, ly)
      # Update port positions:
      nInputs = len(self.inputs)
      nOutputs = len(self.outputs)
      nMulti = len(self.multis)
      dHinput = h / float(nInputs + 1.0)
      dHoutput = h / float(nOutputs + 1.0)
      dWmulti  = w / float( nMulti + 1.0 )
      inputCenters = range(1,nInputs+1) 
      outputCenters   = range(1,nOutputs+1) 
      multiCenters = range(1,nMulti+1)
      for center, p in zip(inputCenters , self.inputs.values()):
          p.setPos( -4 , center*dHinput  )
      for cent , p in zip( outputCenters , self.outputs.values() ):
          p.setPos(w+4 , cent*dHoutput)
      for cent , p in zip( multiCenters , self.multis.values() ):
          p.setPos( cent*dWmulti ,0)
      
     

      self.w = w
      self.h = h
      return w, h
    


# Block part:
class HandleItem(QGraphicsEllipseItem):
   """ A handle that can be moved by the mouse """
   def __init__(self, parent=None):
      super(HandleItem, self).__init__(QRectF(-4.0,-4.0,8.0,8.0), parent)
      self.posChangeCallbacks = []
      self.setBrush(QBrush(Qt.white))
      self.setFlag(self.ItemIsMovable, True)
      self.setFlag(self.ItemSendsScenePositionChanges, True)
      self.setCursor(QCursor(Qt.SizeFDiagCursor))

   def itemChange(self, change, value):
      if change == self.ItemPositionChange:
         x, y = value.x(), value.y()
         # TODO: make this a signal?
         # This cannot be a signal because this is not a QObject
         for cb in self.posChangeCallbacks:
            res = cb(x, y)
            if res:
               x, y = res
               value = QPointF(x, y)
         return value
      # Call superclass method:
      return super(HandleItem, self).itemChange(change, value)

class ParameterDialog(QDialog):
   def __init__(self, parent=None):
      super(ParameterDialog, self).__init__(parent)
      self.button = QPushButton('Ok', self)
      l = QVBoxLayout(self)
      l.addWidget(self.button)
      self.button.clicked.connect(self.OK)
   def OK(self):
      self.close()
