from coordinate import Coordinate
class Selection:
    def __init__(self, start:Coordinate=Coordinate(), end:Coordinate=Coordinate()):
        self.start, self.end = Coordinate.getOrderedList(start, end)

    def __str__(self):
        return "%s to %s"%(self.start, self.end)

    def toList(self):
        return [list(range(getattr(self.start, axis), getattr(self.end, axis) + 1)) for axis in ("x", "y", "z")]

    def __iter__(self):
        self.__current_x = self.start.x
        self.__current_y = self.start.y
        self.__current_z = self.start.z
        return self

    def __next__(self):
        coordinate = Coordinate(self.__current_x, self.__current_y, self.__current_z)
        if self.__current_x > self.end.x:
            raise StopIteration
        elif self.__current_y == self.end.y:
            self.__current_x += 1
            self.__current_y = self.start.y
        elif self.__current_z == self.end.z:
            self.__current_y += 1
            self.__current_z = self.start.z
        else:
            self.__current_z += 1
        
        return coordinate



class BlocksSelection(Selection):
    def toChunksSelection(self):
        coordinates = []
        for coordinate in [self.start, self.end]:
            coordinates += [Coordinate(xyz_list=(list(map(lambda c : c >> 4, coordinate.toTuple()))))]
        return ChunksSelection(start=coordinates[0], end=coordinates[1])

    def toRegionsSelection(self):
        return self.toChunksSelection().toRegionsSelection()

class ChunksSelection(Selection):
    def toBlocksSelection(self):
        coordinates = []
        coordinates += [Coordinate(xyz_list=(list(map(lambda c : c << 4, self.start.toTuple()))))]
        coordinates += [Coordinate(xyz_list=(list(map(lambda c : (c + 1 << 4) - 1, self.end.toTuple()))))]
        return BlocksSelection(start=coordinates[0], end=coordinates[1])
    
    def toRegionsSelection(self):
        coordinates = []
        for coordinate in [self.start, self.end]:
            coordinates += [Coordinate(xyz_list=(list(map(lambda c : c >> 5, coordinate.toTuple()))))]
        return RegionsSelection(start=coordinates[0], end=coordinates[1])

class RegionsSelection(Selection):
    def toBlocksSelection(self):
        self.toChunksSelection().toBlocksSelection()

    def toChunksSelection(self):
        coordinates = []
        coordinates += [Coordinate(xyz_list=(list(map(lambda c : c << 5, self.start.toTuple()))))]
        coordinates += [Coordinate(xyz_list=(list(map(lambda c : (c + 1 << 5) - 1, self.end.toTuple()))))]
        return ChunksSelection(start=coordinates[0], end=coordinates[1])
