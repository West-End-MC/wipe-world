class Coordinate:
    def __init__(self, x:int=0, y:int=0, z:int=0, xyz_list:list=None):
        if xyz_list is not None:
            self.x, self.y, self.z = xyz_list
        else:
            self.x = x
            self.y = y
            self.z = z
    
    def toList(self):
        return [ self.x, self.y, self.z ]

    def toTuple(self):
        return ( self.x, self.y, self.z )

    def toDict(self):
        return { "x":self.x, "y":self.y, "z":self.z }

    def __iter__(self):
        self.__current_index = -1
        return self

    def __next__(self):
        if self.__current_index >= 2:
            raise StopIteration
        Coordinate = self.toDict()
        self.__current_index += 1
        Coordinate_axis  = list(Coordinate.keys())[self.__current_index]
        Coordinate_value = Coordinate[Coordinate_axis]
        return {"axis":Coordinate_axis, "value":Coordinate_value}
    
    def __str__(self):
     return "%s %s %s"%(self.x, self.y, self.z)

    @staticmethod
    def getOrderedList(first:"Coordinate", second:"Coordinate"):
        Coordinates = [Coordinate(), Coordinate()]
        for axis in first:
            if axis["value"] < getattr(second, axis["axis"]):
                setattr(Coordinates[0], axis["axis"], axis["value"])
                setattr(Coordinates[1], axis["axis"], getattr(second, axis["axis"]))
            else:
                setattr(Coordinates[0], axis["axis"], getattr(second, axis["axis"]))
                setattr(Coordinates[1], axis["axis"], axis["value"])
        return Coordinates
