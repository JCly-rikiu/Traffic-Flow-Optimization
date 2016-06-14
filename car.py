# car.py

import Queue
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
        self.mapInfo = mapLayout.mapInfo
        self.intersections = mapLayout.intersections
        self.crossroads = mapLayout.crossroads
        self.roads = mapLayout.roads
        self.cars = []
        # self.trafficlight = TrafficLight
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

    def getDirection(self, start, end):
        (startRoad, si) = self.getRoadIndex(start[0], start[1])
        (endRoad, ei) = self.getRoadIndex(end[0], end[1])

        distance = 0
        sameway = True if startRoad == endRoad and si > ei else False

        prev = {}
        pq = Queue.PriorityQueue()
        pq.put((0, startRoad))
        twice = sameway
        while not pq.empty():
            (dist, number) = pq.get()
            if number == endRoad:
                if twice:
                    twice = False
                else:
                    distance = dist
                    break
            road = self.roads[number]
            dist += road.getDistance()
            (nodeType, nodeNum) = road.getEnd()
            if nodeType == Info.INTERSECTION:
                node = self.intersections[nodeNum]
            elif nodeType == Info.CROSSROAD:
                node = self.crossroads[nodeNum]
            for rn in node.getOutRoads():
                if rn not in prev:
                    prev[rn] = number
                    pq.put((dist, rn))

        now = endRoad
        direction = [now]
        twice = sameway
        while True:
            if now == startRoad:
                if twice:
                    twice = False
                else:
                    break
            now = prev[now]
            direction.append(now)

        direction.reverse()
        result = [(r, self.roads[r].getDistance()) for r in direction]
        result[0] = (result[0][0], result[0][1] - si)
        result[-1] = (result[-1][1], ei)
        return (distance + ei - si, result)

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

    def moveTo(self, number, roadNumber, tick):
        car = self.cars[number]
        (r, i) = car.roadIndex
        road = self.roads[r]
        if road.getDistance() != i + 1:
            return (self.NOT_AT_THE_END_OF_ROAD)
        # TODO Traffic light
        #
        #   return (self.BLOCKED_BY_TRAFFIC_LIGHT)
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
    print(cm.getDirection((4, 4), (8, 4)))
