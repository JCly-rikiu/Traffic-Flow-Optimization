# layout.py

from game import Info, Intersection, Crossroad
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
        self.parseRoad(layoutText)

    def parseMap(self, layoutText):
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[y][x]
                if (not self.mapInfo.get(x, y) is None): continue
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
            if (not self.mapInfo.get(nextX, nextY) is None): continue
            positions.extend(self.parseIntersection(layoutText, nextX, nextY, number))
        return positions

    def parseCrossroad(self, layoutText, x, y, number):
        self.mapInfo.setCrossroad(x, y, number)
        positions = [(x, y)]
        for (nextX, nextY) in self.getPosNearBy(x, y):
            if layoutText[nextY][nextX] != 'C': continue
            if (not self.mapInfo.get(nextX, nextY) is None): continue
            positions.extend(self.parseCrossroad(layoutText, nextX, nextY, number))
        return positions

    def parseRoad(self, layoutText):
        pass

    def getPosNearBy(self, x, y):
        position = []
        move = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for m in move:
            nextX = x + m[0]
            nextY = y + m[1]
            if 0 <= nextX < self.width and 0 <= nextY < self.height:
                position.append((nextX, nextY))
        return position


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
    if (not os.path.exists(fullname)): return None
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
