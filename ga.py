# ga.py

from random import randint

class Gene:
    def __init__(self, trafficInfo, randomGenerate=True):
        self.geneStr = ""
        self.geneLen = 0
        self.matched = {}
        self.roadToLight = {}
        self.roadInfo = {}
        self.lightInfo = {}
        if randomGenerate:
            self.buildUpGene(trafficInfo)

    def buildUpGene(self, trafficInfo):
        for trafficLight, intersections in trafficInfo:
            self.geneLen += len(intersections)
            lightlist = []
            for _ in range(len(intersections)):
                duration = randint(1, 10)
                lightlist.append(duration)
                self.geneStr += "{0:02d}".format(duration)

            self.lightInfo[trafficLight] = lightlist
            self.roadInfo[trafficLight] = intersections
            for road in intersections:
                self.roadToLight[road] = trafficLight

# trafficInfo is look like:
#   [(0, [2, 4, 6, 8]), (1, [1, 3, 5, 7])]

class GeneInfo:
    def __init__(self, gene):
        self.gene = gene

    def isGreen(self, road, tick):
        intersection = self.gene.roadToLight[road]
        roadlist = self.gene.roadInfo[intersection]
        lightlist = self.gene.lightInfo[intersection]
        cycle = sum(lightlist)
        tick = tick % cycle
        for i in range(len(roadlist)):
            if tick > lightlist[i]:
                tick -= lightlist[i]
            elif road == roadlist[i]:
                return True
            else:
                return False
        return False


# trafficInfo = [(0, [2, 4, 6, 8]), (1, [1, 3, 5, 7])]
