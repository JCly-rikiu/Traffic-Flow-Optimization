# layout.py

from game import Info, Intersection, Crossroad, Road
import os

class Layout:
    """
    A Layout parse the map into Graph.
    """

    def __init__(self, layoutText):
        self.width = len(layoutText[0])
        self.height = len(layoutText)
        self.mapInfo = Info(self.width, self.height)
        self.intersections = []
        self.crossroads = []
        self.roads = []
        self.parseLayoutText(layoutText)
        self.layoutText = layoutText

    def parseLayoutText(self, layoutText):
        """
        Parse all intersections and crossroads first, and then parse the roads in the map.
        """

        self.parseMap(layoutText)
        self.parseMap2(layoutText)

    def parseMap(self, layoutText):
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[y][x]
                if not (self.mapInfo.get(x, y) is None): continue
                if layoutChar == '%':
                    self.mapInfo.setField(x, y)
                elif layoutChar == 'I':
                    number = len(self.intersections)
                    positions = self.parseIntersection(layoutText, x, y, number)
                    self.intersections.append(Intersection(number, positions))
                elif layoutChar == 'C':
                    number = len(self.crossroads)
                    positions = self.parseCrossroad(layoutText, x, y, number)
                    self.crossroads.append(Crossroad(number, positions))

    def parseIntersection(self, layoutText, x, y, number):
        self.mapInfo.setIntersection(x, y, number)
        positions = [(x, y)]
        for (nextX, nextY) in self.getPosNearBy(x, y):
            if layoutText[nextY][nextX] != 'I': continue
            if not (self.mapInfo.get(nextX, nextY) is None): continue
            positions.extend(self.parseIntersection(layoutText, nextX, nextY, number))
        return positions

    def parseCrossroad(self, layoutText, x, y, number):
        self.mapInfo.setCrossroad(x, y, number)
        positions = [(x, y)]
        for (nextX, nextY) in self.getPosNearBy(x, y):
            if layoutText[nextY][nextX] != 'C': continue
            if not (self.mapInfo.get(nextX, nextY) is None): continue
            positions.extend(self.parseCrossroad(layoutText, nextX, nextY, number))
        return positions

    def parseMap2(self, layoutText):
        for node in self.intersections + self.crossroads:
            for pos in node.getPostions():
                for (nextX, nextY) in self.getPosNearBy(pos[0], pos[1]):
                    if not (self.mapInfo.get(nextX, nextY) is None): continue
                    (testX, testY) = self.getNextPos(nextX, nextY, layoutText[nextY][nextX])
                    if not (testX == pos[0] and testY == pos[1]):
                        number = len(self.roads)
                        positions = self.parseRoad(layoutText, nextX, nextY, number)
                        start = self.mapInfo.get(pos[0], pos[1])
                        end = positions.pop()
                        self.roads.append(Road(number, positions, start, end))

    def parseRoad(self, layoutText, x, y, number):
        self.mapInfo.setRoad(x, y, number)
        positions = [(x, y)]
        (nextX, nextY) = self.getNextPos(x, y, layoutText[y][x])
        posInfo =  self.mapInfo.get(nextX, nextY)
        if posInfo is None:
            positions.extend(self.parseRoad(layoutText, nextX, nextY, number))
        else:
            positions.append(posInfo)
        return positions

    def getPosNearBy(self, x, y):
        positions = []
        move = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for m in move:
            nextX = x + m[0]
            nextY = y + m[1]
            if 0 <= nextX < self.width and 0 <= nextY < self.height:
                positions.append((nextX, nextY))
        return positions

    def getNextPos(self, x, y, direction):
        if direction == 'N':
            return (x, y - 1)
        elif direction == 'S':
            return (x, y + 1)
        elif direction == 'E':
            return (x + 1, y)
        elif direction == 'W':
            return (x - 1, y)

# Call by Game?
def getLayout(name, back=2):
    if name.endswith('.lay'):
        layout = tryToLoad('layouts/' + name)
        if layout is None: layout = tryToLoad(name)
    else:
        layout = tryToLoad('layouts/' + name + '.lay')
        if layout is None: layout = tryToLoad(name + '.lay')
    if layout == None and back >= 0:
        curdir = os.path.abspath('.')
        os.chdir('..')
        layout = getLayout(name, back - 1)
        os.chdir(curdir)
    return layout

def tryToLoad(fullname):
    if not os.path.exists(fullname): return None
    f = open(fullname)
    try: return Layout([line.strip() for line in f])
    finally: f.close()

if __name__ == '__main__':
    l = getLayout('test')
    print('crossroads')
    for c in l.crossroads:
        print(c.getPostions())
    print('intersections')
    for i in l.intersections:
        print(i.getPostions())
    print('roads')
    for r in l.roads:
        print(r.getPostions())
        print(r.getStart())
        print(r.getEnd())
