class NameManager( ):
    def __init__(self ):
        self.namelist =[]
    def GetUnique(self , name ):
        idx = 0;
        returnName = name + str(idx)
        while( returnName in self.namelist ):
            idx = idx + 1
            returnName = name + "_" + str(idx)
        self.namelist.append( returnName )
        return returnName
    def Remove( self , name ):
        self.namelist.remove( name )