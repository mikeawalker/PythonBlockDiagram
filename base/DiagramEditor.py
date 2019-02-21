from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import xml.etree.ElementTree as ET
from xml.dom import minidom
from base.Block import *
from pathlib import Path
from base.Library import *
from base.Connection import *
import Tools as Tools
import copy as Copy
class DiagramScene(QGraphicsScene ):
   def __init__(self, editor , lib , parent=None):
      super(DiagramScene, self).__init__(parent)
      self.editor = editor
      self.library = lib
      self.nameManager = Tools.NameManager()
      self.blockList = dict()
   def mouseMoveEvent(self, mouseEvent):
      self.editor.sceneMouseMoveEvent(mouseEvent)
      super(DiagramScene, self).mouseMoveEvent(mouseEvent)
   def mouseReleaseEvent(self, mouseEvent):
      self.editor.sceneMouseReleaseEvent(mouseEvent)
      super(DiagramScene, self).mouseReleaseEvent(mouseEvent)
   def AddBlock(self , type , position ):
         # Get the data of the block from the library        
         #make the block item  
         blocktree = self.library.getBlockDef( type )
         # We want to --copy-- the tree so that we have our own per block
         c = Copy.deepcopy( blocktree )
         # get the name from the block tree
         n = c.get("Name")
         n = self.nameManager.GetUnique(n)
         c.set("Name",n)
         block = BlockItem(c , self.editor )
         self.addItem(block)
         block.setPos(position)

         self.blockList[n] = block
         return block
   def GetBlock( self , name ):
       block = self.blockList[name]
       return block
   
   def RemoveBlock( self , name ):
        block = self.blockList[name]
        x= self.blockList.pop(name , None)
        self.removeItem(x)
        self.nameManager.Remove(name)
   def MakeDiagramTree( self ,base):
       for blockName in self.blockList:
           block = self.blockList[blockName]
           blockTree= block.getTree()
           base.append( blockTree )
       
class DiagramEditor(QWidget ):
   def __init__(self, extender,  parent=None):
      QWidget.__init__(self, parent)
      extender.SetEditor( self )
      self.connectionList = []
      self.setWindowTitle("Diagram editor")
      self.extender = extender
      # Widget layout and child widgets:
      self.horizontalLayout = QHBoxLayout(self)
      self.libraryBrowserView = QListView(self)
      self.libraryModel = LibraryModel(self)
      self.libraryModel.setColumnCount(1)


     
      self.libraryBrowserView.setModel(self.libraryModel)
      self.libraryBrowserView.setViewMode(self.libraryBrowserView.IconMode)
      self.libraryBrowserView.setDragDropMode(self.libraryBrowserView.DragOnly)

      self.diagramScene = DiagramScene(self ,  self.libraryModel , self )
      self.diagramView = EditorGraphicsView(self.diagramScene, self)
      self.horizontalLayout.addWidget(self.libraryBrowserView)
      self.horizontalLayout.addWidget(self.diagramView)




      self.startedConnection = None

      self.setupMenus()
   def setupMenus( self  ):
      # Menu Bar
      self.myQMenuBar = QMenuBar(self)
      # File Munu
      fileMenu = self.myQMenuBar.addMenu('File')
      exitAction = QAction('Exit', self)        #Quit
      exitAction.setShortcut("Ctrl+Q")
      exitAction.setStatusTip("EXIT")
      exitAction.triggered.connect(qApp.quit)  #Quit
      openAction = QAction('Open', self)        #Open
      openAction.setShortcut("Ctrl+O")
      openAction.setStatusTip("Open FIle")
      openAction.triggered.connect(self.open)  #Open
      saveAction = QAction('Save', self)        #Save
      saveAction.setShortcut("Ctrl+S")
      saveAction.setStatusTip('Save File')
      saveAction.triggered.connect(self.save)  #Open

      #saveAction.triggered.connect(qApp.quit)  #Save
      fileMenu.addAction(openAction)
      fileMenu.addAction(saveAction)
      fileMenu.addAction(exitAction)
      # Library Menu
      libraryMenu = self.myQMenuBar.addMenu('Library')
      loadAction = QAction('LoadLib', self)        #LoadLib
      loadAction.setShortcut("Ctrl+L")
      loadAction.setStatusTip("Load Library")
      loadAction.triggered.connect( self.libraryModel.LoadLibrary)  #LoadLib

      libraryMenu.addAction(loadAction)
      
      self.extender.ExtraMenuItems( self.myQMenuBar   )
   def ConstructSave( self ):
       base = ET.Element( "diagram" ) 
       self.diagramScene.MakeDiagramTree(base)
       self.libraryModel.GetLibraries( base )
       for connection in self.connectionList:
           e = connection.getTree()
           base.append( e )
       return base
   def save( self  ):
        name = QFileDialog.getSaveFileName(self, 'Save File')
        tree = self.ConstructSave( )
        rough_string = ET.tostring(tree, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        strOut      = reparsed.toprettyxml(indent="  ")
        
        with open("_work/DiagramIntermediateOutput.xml", "w") as f:
            f.write(strOut)
        # extender.TranslateToData( tree )
   def open( self ):
       name = QFileDialog.getOpenFileName(self, "Open File")
       tree = ET.parse(name[0])
       root = tree.getroot()
       for lib in root.findall("LibraryFile"):
           self.libraryModel.LoadLib( lib.text )
       for block in root.findall("Block"):
           name = block.find("Name").text
           type = block.find("Type").text
           lib  = block.find("Library").text
           posx = float(block.get("X"))
           posy = float(block.get("Y"))
           pos  = QPointF(posx,posy)
           b = self.diagramScene.AddBlock(type , pos)
          
           
       for connect in root.findall("Connection"):
           start = connect.get("Begin").split("/")
           end   = connect.get("End").split("/")
           startBlock = start[0]
           endBlock   = end[0]
           startPort  = start[1]
           endPort    = end[1]
           portS = self.diagramScene.GetBlock(startBlock).GetPort(startPort)
           portE = self.diagramScene.GetBlock(endBlock).GetPort(endPort)
           c = Connection( portS )
           c.SetPort( portE )
           c.Refresh()
           self.connectionList.append( c )
   def startConnection(self, port):
      self.startedConnection = Connection(port)
      return self.startedConnection
   def sceneMouseMoveEvent(self, event):
      if self.startedConnection:
         pos = event.scenePos()
         self.startedConnection.setEndPos(pos)
   def sceneMouseReleaseEvent(self, event):
      # Clear the actual connection:
      good = False
      if self.startedConnection:
         pos = event.scenePos()
         items = self.diagramScene.items(pos)
         for item in items:
            if type(item) is PortItem:
               good = self.startedConnection.SetPort(item)
               self.connectionList.append( self.startedConnection )
         if not good:
            self.startedConnection.delete()
         self.startedConnection = None
class EditorGraphicsView(QGraphicsView):
   def __init__(self, scene, parent=None):
      QGraphicsView.__init__(self, scene, parent)
      self.theScene = scene
   def dragEnterEvent(self, event):
      x= event.mimeData().text
      if event.mimeData().hasFormat('Block'):
         event.accept()
   def dragMoveEvent(self, event):
      if event.mimeData().hasFormat('Block'):
         event.accept()
   def dropEvent(self, event):
      if event.mimeData().hasFormat('Block'):
         name = str(event.mimeData().data('Block') )
         name = event.mimeData().text()
         position = self.mapToScene(event.pos())
         self.theScene.AddBlock( name , position )
