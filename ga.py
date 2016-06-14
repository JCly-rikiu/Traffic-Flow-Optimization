# ga.py

from random import randint

class Gene:
    def __init__(self, trafficInfo, randomGenerate=True):
        self.geneStr = ""
        self.geneLen = 0
        self.matched = {}
        if randomGenerate:
            self.buildUpGene(trafficInfo)

    def buildUpGene(self, trafficInfo):
        matchedIndex = 0
        for trafficLight, intersections in trafficInfo:
            self.geneLen += len(intersections)
            for _ in range(len(intersections)):
                self.geneStr += "{0:02d}".format(randint(1, 10))
            for road in intersections:
                self.matched[road] = matchedIndex
                matchedIndex += 1

    def getUnitTime(self, road):
        pos = self.matched[road]
        return int(self.geneStr[pos*2 : pos*2+2])

trafficInfo = [(0, [2, 4, 6, 8]), (1, [1, 3, 5, 7])]
g = Gene(trafficInfo)
print "geneLen =", g.geneLen
print "geneStr =", g.geneStr

print g.getUnitTime(1)
print g.getUnitTime(2)
print g.getUnitTime(3)
print g.getUnitTime(4)
print g.getUnitTime(5)
print g.getUnitTime(6)
print g.getUnitTime(7)
print g.getUnitTime(8)
