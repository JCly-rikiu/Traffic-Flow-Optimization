# ga.py

from random import randint

class Gene:
    def __init__(self, trafficInfo, randomGenerate=True, geneStr=""):
        self.geneStr = ""
        self.geneLen = 0
        self.trafficInfo = trafficInfo
        self.matched = {}
        self.roadToLight = {}
        self.roadInfo = {}
        self.lightInfo = {}
        if randomGenerate:
            self.buildUpGene()
        else:
            self.buildFromStr(geneStr)

    def buildUpGene(self):
        for trafficLight, intersections in self.trafficInfo:
            self.geneLen += len(intersections)
            lightlist = []
            for _ in range(len(intersections)):
                duration = randint(2, 10)
                lightlist.append(duration)
                self.geneStr += "{0:02d}".format(duration)

            self.lightInfo[trafficLight] = lightlist
            self.roadInfo[trafficLight] = intersections
            for road in intersections:
                self.roadToLight[road] = trafficLight

    def buildFromStr(self, geneStr):
        index = 0
        self.geneStr = geneStr
        for trafficLight, intersections in self.trafficInfo:
            self.geneLen += len(intersections)
            lightlist = []
            for _ in range(len(intersections)):
                duration = int(geneStr[i*2 : i*2 + 2])
                lightlist.append(duration)
                index += 1

            self.lightInfo[trafficLight] = lightlist
            self.roadInfo[trafficLight] = intersections
            for road in intersections:
                self.roadToLight[road] = trafficLight

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

class GeneEvolve:
    @classmethod
    def evolve(cls, g1, g2, mutateRate=0.1):
        newGen = cls.merge(g1, g2)
        geneStr = cls.mutate(newGen, mutateRate)
        return Gene(g1.trafficInfo, False, geneStr)

    @classmethod
    def merge(cls, g1, g2):
        newGen = ""
        genLen = len(g1.geneStr)
        geneStr = [g1.geneStr, g2.geneStr]
        for i in range( len(gs1)/2 ):
            newGen += geneStr[randint(0,1)][i*2 : i*2 + 2]
        return newGen

    @classmethod
    def mutate(cls, geneStr, mutateRate):
        for i in randint(0, int(len(geneStr)/2 * mutateRate) ):
            pos = randint(0, len(geneStr)/2)
            geneStr = geneStr[: pos*2] + "{0:02d}".format(randint(2,10)) + geneStr[pos*2+2 :]
        return geneStr
