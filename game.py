# game.py

class Info:
    """
    A 2-dimensional array to store the map information.
    """

    FIELD = 'Field'
    INTERSECTION = 'Intersection'
    CROSSROAD = 'Crossroad'
    ROAD = 'Road'

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[None for _ in range(height)] for _ in range(width)]

    def get(self, x, y):
        return self.data[x][y]

    def setField(self, x, y):
        self.data[x][y] = (self.FIELD)

    def setIntersection(self, x, y, number):
        self.data[x][y] = (self.INTERSECTION, number)

    def setCrossroad(self, x, y, number):
        self.data[x][y] = (self.CROSSROAD, number)

    def setRoad(self, x, y, number):
        self.data[x][y] = (self.ROAD, number)

class Intersection:
    """
    An intersecion in the map.
    """

    def __init__(self, number, positions):
        self.number = number
        self.positions = positions

    def getPostions(self):
        return self.positions

    def addInRoad(self):
        pass

    def addOutRoad(self):
        pass

class Crossroad:
    """
    A crossroad in the map.
    """

    def __init__(self, number, positions):
        self.number = number
        self.positions = positions

    def getPostions(self):
        return self.positions

    def addInRoad(self):
        pass

    def addOutRoad(self):
        pass

class Road:
    """
    A road in the map.
    """

    def __init__(self, number, positions, start, end):
        self.number = number
        self.positions = positions
        self.start = start
        self.end = end

    def getPostions(self):
        return self.positions

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getDistance(self):
        return len(self.positions)
