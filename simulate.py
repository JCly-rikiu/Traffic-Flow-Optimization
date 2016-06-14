# car.py

from car import CarMap

class Car(object):
    """
    A car in simulation.
    """

    def __init__(self, idd, dirs):
        self.stepLeft = dirs[0]
        self.dirs = dirs[1]
        self.timeStamp = 0

    def isArrived(self):
        return self.stepLeft == 0

    def nextRoad(self):
        if self.dirs[0][1] == 1 and self.stepLeft != 1:
            return self.dirs[0][0] # id of next new road
        return -1 # no need to change road

    def move(self):
        self.stepLeft -= 1
        if self.dirs[0][1] == 1:
            del self.dirs[0]
        else:
            self.dirs[0] = (self.dirs[0][0], self.dirs[0][1] - 1)

class Simulation(object):

    def __init__(self, startEndList, carMap):
        self.carN = len(startEndList)
        self.cm = carMap
        self.cm.initialCars([startEndList[i][0] for i in range(self.carN)])
        self.cars = []
        for i in range(self.carN):
            self.cars.append(Car(i, self.cm.getDirection(startEndList[i][0], startEndList[i][1])))
        self.carCnt = self.carN
        self.tick = 0

    def run(self):
        while self.carCnt:
            self.tick += 1
            for i in range(self.carN):
                self.moveCarRecursively(i)
        self.cm.clearAllCars()
        for i in range(self.carN):
            print "Car", i, "takes", self.cars[i].timeStamp, "ticks."

    def makeAMove(self, i, nextRoad):
        if nextRoad == -1:
            return self.cm.move(i)
        return self.cm.moveTo(i, nextRoad, self.tick)

    def moveCarRecursively(self, i):
        if self.cars[i].isArrived() or self.cars[i].timeStamp == self.tick:
            return
        self.cars[i].timeStamp = self.tick
        nextRoad = self.cars[i].nextRoad()
        state = self.makeAMove(i, nextRoad)
        if state[0] == CarMap.BLOCKED_BY_OTHER_CAR:
            self.moveCarRecursively(state[1])
            state = self.makeAMove(i, nextRoad)
        if state[0] == CarMap.SUCCESS:
            self.cars[i].move()
            if self.cars[i].isArrived():
                self.cm.remove(i)
                self.carCnt -= 1

if __name__ == '__main__':
    Simulation([((7, 4), (10, 4))], 'face').run()
