from abc import ABC, abstractmethod
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class ArrowItem(ABC):
    def __init__(self , nItems , color = Qt.red ):
        super().__init__()
        self.arrows = []
        for k in range(0,nItems ):
            self.arrows.append( QGraphicsLineItem() )
        for arrow in self.arrows:
            arrow.setPen(QPen(color , 2))    
    @abstractmethod
    def Update(self , start , end ):
        pass
    def Add(self , scene ):
        for arrow in self.arrows:
            scene.addItem( arrow )
    def Remove(self , scene ):
        for arrow in self.arrows:
            scene.removeItem( arrow )
    def MakeDir(self , point , dir ,len ):
        xx = { "Left" : len , "Right" : - len }
        X = xx[dir]
        pA = QPointF( point.x() + X , point.y()+len )
        pB = QPointF( point.x() + X , point.y()-len )
        LineA = QLineF( point , pA)
        LineB = QLineF( point , pB)
        return [LineA,LineB]

class OneWayArrow(ArrowItem):
    def __init__(self ):
        super().__init__( 5 )
       
    def Update(self, start, end):
       midX = (end.x() - start.x())/2 + start.x()
       p1   = start
       p2   = QPointF( midX , start.y());
       p3   = QPointF( midX , end.y());
       p4   = end
       self.arrows[0].setLine( QLineF(p1, p2) )
       self.arrows[1].setLine( QLineF(p2, p3) )
       self.arrows[2].setLine( QLineF(p3, p4) )
       # arrow 
       endArrow = self.MakeDir( end, "Right" , 7)
       self.arrows[3].setLine( endArrow[0])
       self.arrows[4].setLine( endArrow[1])
       
class TwoWayArrow(OneWayArrow):
    def __init__(self):
        super().__init__()
        self.arrows.append(QGraphicsLineItem())
        self.arrows.append(QGraphicsLineItem())
    def Update( self , start , end ):
        super().Update( start , end )
        #twodo --- make it a circle? 
        startArrow = self.MakeDir( start , "Left" , 7)
        self.arrows[5].setLine(  startArrow[0] )
        self.arrows[6].setLine( startArrow[1] )