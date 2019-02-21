from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from base.ArrowGroup import *
from math import *
import xml.etree.ElementTree as ET

class Connection:
   """
    - fromPort
    - toPort
   """
   def __init__(self, port):
      self.color = Qt.red
      self.editor = port.editor
      self.pos1 = None
      self.pos2 = None
      self.startPortSet = False
      self.stopPortSet  = False
      self.ports =[]
      self.ports.append( port )

      if port:
         self.pos1 = port.scenePos()
      self.toPort = None
      # Create arrow item:
      if( port.getDirection() == "TwoWay"):
          self.arrow = TwoWayArrow()
      else:
          self.arrow = OneWayArrow()
      self.arrow.Add( self.editor.diagramScene )
      
   def getTree( self ):
       e = ET.Element("Connection")
       e.set("Begin" , self.startName )
       e.set("End"   , self.stopName)
       return e
   def VerifyConnect( self  ):
       ret = False
       directions = [self.ports[0].getDirection() , self.ports[1].getDirection()]
       acceptable = [["In","Out"] , ["Out","In"], ["TwoWay","TwoWay"]]
       if( directions in acceptable ):
           print("Valid Connection Attempt")
           ret = True
       else:
          error = "Bad Connection attempt between ports with types: " + str(directions)
          print( error )
          #TODO PoP a window warning

       if( directions[0] == "In"):
           start = 0
           stop  = 1
       else:
           start = 1
           stop  = 0
       self.startName = self.ports[start].GetName()
       self.stopName = self.ports[stop].GetName()
       return ret
   def SetPort( self  , port ):
       ret = False
       self.ports.append( port )
       if( self.VerifyConnect() ):
           if( self.ports[0].getDirection() is "Multi" ):
               p1 = self.ports[0]
               p2 = self.ports[1]
           elif(self.ports[0].getDirection() is "Out"):
               p1 = self.ports[0]
               p2 = self.ports[1]
           else:
               p1 = self.ports[1]
               p2 = self.ports[0]
           p1.connect( self )
           p2.connect( self )
           self.setFromPort(p1)
           self.setToPort(p2)
           ret = True
       else:
           self.toPort = None
           self.fromPort = None
       return ret


   def setFromPort(self, fromPort):
      self.fromPort = fromPort
      self.pos1 = fromPort.scenePos()
      self.fromPort.posCallbacks.append(self.setBeginPos)
   def setToPort(self, toPort):
      self.toPort = toPort
      self.pos2 = toPort.scenePos()
      self.toPort.posCallbacks.append(self.setEndPos)
   def setEndPos(self, endpos):
      self.pos2 = endpos
      self.arrow.Update( self.pos1, self.pos2 )
   def setBeginPos(self, pos1):
      self.pos1 = pos1
      self.arrow.Update( self.pos1, self.pos2)
   def delete(self):
      #self.editor.diagramScene.removeItem(self.arrow)
      self.arrow.Remove( self.editor.diagramScene )
      # Remove position update callbacks:
   def Refresh(self):
       self.arrow.Update(self.pos1, self.pos2)
