from abc import ABC, abstractmethod


class Extender(ABC):
    def __init__(self , name ):
        print("Extender attached --- " + name )
    def SetEditor( self , editor ):
        self.editor = editor
    def LoadBlockLibrary( self , dataTree):
        # Verify the data is compliant
        self.Verify( dataTree )
        # Translate the data to a diagram tree
        self.diagramTree = self.TranslateToDiagram( dataTree )
        return self.diagramTree
    @abstractmethod   
    def TranslateToDiagram( self , dataTree ):
        pass
    @abstractmethod 
    def TranslateToData( self , diagramTree ):
        pass
    def BlockRightClick( self , menu ):
        print("Extra Block Right Click")
    def PortRightClick( self ):
        print("Extra Port Right Click")
    def ExtraMenuItems( self , menuBar  ):
        print("Extra Menu Items")



