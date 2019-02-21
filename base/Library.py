from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import xml.etree.ElementTree as ET
import Tools as Tools

class LibraryItem(QStandardItem):
    def __init__(self , root,  parent=None):
        name = root.get("Name")
        type = root.find("Type").text
        super().__init__(QIcon(self.Paint()),type)
        self.itemTree = root

    def Paint(self):
      # Create an icon with an icon:
      pixmap = QPixmap(60, 60)
      pixmap.fill()
      painter = QPainter(pixmap)
      painter.fillRect(10, 10, 40, 40, Qt.blue)
      painter.setBrush(Qt.red)
      painter.drawEllipse(36, 2, 20, 20)
      painter.setBrush(Qt.yellow)
      painter.drawEllipse(20, 20, 20, 20)
      painter.end()
      return pixmap
class LibraryModel(QStandardItemModel):
   def __init__(self, parent=None):
      QStandardItemModel.__init__(self, parent)
      self.blockDictionary = dict()
      self.names = Tools.NameManager()
      self.libList = []
   def mimeTypes(self):
      return ['Block']
   def GetLibraries( self , base ):
       for lib in self.libList:
           e = ET.Element("LibraryFile")
           e.text = lib
           base.append( e )
   def LoadLib( self , filename):
      self.libList.append( filename )
      tree = ET.parse(filename)
      root = tree.getroot()
      for block in root.findall('Block'): 
          self.AddLibraryItem(block)
   def LoadLibrary(self , filename ):
      w = QWidget()
      filename = QFileDialog.getOpenFileName(w, 'Load Library', './')
      self.LoadLib( filename[0] )
   def AddLibraryItem( self , itemTree ):
       # get the default name
       name = itemTree.get("Name") 
       type = itemTree.find("Type").text
       lib = itemTree.find("Library").text

       # create the item
       newItem = LibraryItem(itemTree)
       #Rename if name exists in dictionary
       print("Appending block Library with library: " + lib + " Type: "+ type  )
       self.blockDictionary[type] = newItem
       self.appendRow(newItem)
   #def DeleteLibraryItem( self , name ):
   def getBlockDef(self , type ):
       return self.blockDictionary[type].itemTree
   def mimeData(self, idxs):
      mimedata = QMimeData()
      for idx in idxs:
         if idx.isValid():
            txt = self.data(idx, Qt.DisplayRole)
            mimedata.setText(txt)
            arr = bytearray(txt, 'utf-8')
            
            mimedata.setData('Block', arr)
      return mimedata

