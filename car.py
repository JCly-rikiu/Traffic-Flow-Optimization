# car.py

from layout import getLayout
from game import Info

class Car(object):
    """
    A car in the map.
    """

    def __init__(self, number, pos, roadIndex):
        self.number = number
        self.pos = pos
        self.roadIndex = roadIndex

    def draw(self):
        pass

class CarMap(object):
    """
    A map to store the positions of cars.
    """

    SUCCESS = 'success'
    BLOCKED_BY_OTHER_CAR = 'blocked by other car'
    BLOCKED_BY_TRAFFIC_LIGHT = 'blocked by traffic light'
    NOT_SELECT_ROAD = 'not select road'
    NOT_AT_THE_END_OF_ROAD = 'not at the end of road'

    def __init__(self, mapLayout):
        if type(mapLayout) == str:
            mapLayout = getLayout(mapLayout)
        self.mapLayout = mapLayout
        self.mapInfo = mapLayout.mapInfo
        self.roads = mapLayout.roads
        self.cars = []
        self.data = [[None for _ in range(r.getDistance())] for r in self.roads]

    def initialCars(self, cars):
        for c in cars:
            (x, y) = c
            (r, i) = self.getRoadIndex(x, y)
            if self.data[r][i] is not None: return False
            number = len(self.cars)
            car = Car(number, c, (r, i))
            self.data[r][i] = car
            self.cars.append(car)
        return True

    def clearAllCars(self):
        self.data = [[None for _ in range(r.getDistance())] for r in self.roads]

    def getInfo(self, x, y):
        return self.mapInfo.get(x, y)

    def getRoadIndex(self, x, y):
        info = self.getInfo(x, y)
        if info[0] != Info.ROAD: return None
        index = self.roads[info[1]].getIndexOfRoad((x, y))
        return (info[1], index)

    def move(self, number):
        car = self.cars[number]
        (r, i) = car.roadIndex
        road = self.roads[r]
        pos = road.getPosByIndex(i + 1)
        if pos is None:
            return (self.NOT_SELECT_ROAD, road.getEnd())
        if self.data[r][i + 1] is not None:
            return (self.BLOCKED_BY_OTHER_CAR, self.data[r][i + 1].number)
        car.pos = pos
        car.roadIndex = (r, i + 1)
        self.data[r][i] = None
        self.data[r][i + 1] = car
        car.draw()
        return (self.SUCCESS, pos)

    def moveTo(self, number, roadNumber):
        car = self.cars[number]
        (r, i) = car.roadIndex
        road = self.roads[r]
        if road.getDistance() != i + 1:
            return (self.NOT_AT_THE_END_OF_ROAD)
        # TODO Traffic light
        if self.data[roadNumber][0] is not None:
            return (self.BLOCKED_BY_OTHER_CAR, self.data[r][i + 1].number)
        pos = self.roads[roadNumber].getPosByIndex(0)
        car.pos = pos
        car.roadIndex = (roadNumber, 0)
        self.data[r][i] = None
        self.data[roadNumber][0] = car
        car.draw()
        return (self.SUCCESS, pos)

if __name__ == '__main__':
    cm = CarMap('test')
    cm.initialCars([(2, 3), (3, 3)])
    print(cm.cars[0].number)
    print(cm.cars[0].pos)
    print(cm.move(0))
