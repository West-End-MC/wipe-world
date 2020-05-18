from coordinate import Coordinate
class Selection:
    def __init__(self, start:Coordinate=Coordinate(), end:Coordinate=Coordinate()):
        self.start, self.end = Coordinate.getOrderedList(start, end)

    def __str__(self):
     return "%s to %s"%(self.start, self.end)

    def toList(self):
        return [list(range(getattr(self.start, axis), getattr(self.end, axis) + 1)) for axis in ("x", "y", "z")]


