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

    def setRoad(self, x, y):
        pass

class Intersection:
    """
    An intersecion in the map.
    """

    def __init__(self, number, positions):
        self.number = number
        self.positions = positions

    def getPostions(self):
        return self.positions

class Crossroad:
    """
    A crossroad in the map.
    """

    def __init__(self, number, positions):
        self.number = number
        self.positions = positions

    def getPostions(self):
        return self.positions
