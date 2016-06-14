#!/usr/bin/env python

from Tkinter import *
from game import Info

class Graphic():
    def __init__(self, graphInfo, carList, trafficlightList, gridsize=10):
        self.master = Tk()
        self.master.title("Traffic Flow Optimization")
        self.frame1 = Frame(self.master)
        self.frame1.pack()
        self.frame2 = Frame(self.master)
        self.frame2.pack()

        wid = graphInfo.width
        hei = graphInfo.height
        data = [[0] * hei for _ in range(wid)]

        self.gridSize = gridsize
        self.width = wid * gridsize
        self.height = hei * gridsize
        self.cars = carList
        self.trafficlights = trafficlightList

        self.canvas = Canvas(self.frame1, width=self.width, height=self.height)
        self.canvas.pack()

        self.initDataFromInfo(graphInfo, data)
        self.drawRoadAndBuilding(data, wid, hei)

        self.quitButton = Button(self.frame2, text="Quit", command=self.quit)
        self.quitButton.grid(row=0, column=0)

        self.graphicItem = []

    def run(self, fps=10):
        self.fps = fps
        self.frameTime = 1000 / self.fps
        self.frame1.after(self.frameTime, self.updateElement)
        self.master.mainloop()

    def initDataFromInfo(self, graphInfo, data):
        for x in range(graphInfo.width):
            for y in range(graphInfo.height):
                dataType = graphInfo.data[x][y][0]
                if dataType == Info.FIELD:
                    data[x][y] = 0
                elif dataType == Info.INTERSECTION:
                    data[x][y] = 2
                elif dataType == Info.ROAD or dataType == Info.CROSSROAD:
                    data[x][y] = 1

    def drawRoadAndBuilding(self, data, wid, hei):
        gridsize = self.gridSize
        for x in range(wid):
            for y in range(hei):
                pos_x = x * gridsize
                pos_y = y * gridsize
                if data[x][y] == 0:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#eee", width=0)
                elif data[x][y] == 2:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#393", width=0)
                else:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#333", width=0)

    def updateElement(self):
        gridsize = self.gridSize
        for item in self.graphicItem:
            self.canvas.delete(item)
        self.graphicItem = []

        for light in self.trafficlights:
            x, y = light.pos
            pos_x = x * gridsize
            pos_y = y * gridsize
            colorToDraw = "#f00"
            if light.isGreen:
                colorToDraw = "#0c0"
            coords = [pos_x+1, pos_y+1, pos_x+gridsize-1, pos_y+gridsize-1]
            self.graphicItem.append(self.canvas.create_rectangle(coords, fill=colorToDraw))

        for car in self.cars:
            if car.display == False:
                continue
            x, y = car.pos
            pos_x = x * gridsize
            pos_y = y * gridsize

            if car.way == "N":
                coords = [pos_x+gridsize/2, pos_y+2, pos_x+2, pos_y+gridsize-2, pos_x+gridsize/2, pos_y+2+gridsize/2, pos_x+gridsize-2, pos_y+gridsize-2]
            elif car.way == "W":
                coords = [pos_x+2, pos_y+gridsize/2, pos_x+gridsize-2, pos_y+gridsize-2, pos_x+2+gridsize/2, pos_y+gridsize/2, pos_x+gridsize-2, pos_y+2]
            elif car.way == "S":
                coords = [pos_x+gridsize/2, pos_y+gridsize-2, pos_x+gridsize-2, pos_y+2, pos_x+gridsize/2, pos_y-2+gridsize/2, pos_x+2, pos_y+2]
            else:
                coords = [pos_x+gridsize-2, pos_y+gridsize/2, pos_x+2, pos_y+2, pos_x-2+gridsize/2, pos_y+gridsize/2, pos_x+2, pos_y+gridsize-2]
            self.graphicItem.append(self.canvas.create_polygon(coords, fill="#f96"))

        self.frame1.after(self.frameTime, self.updateElement)

    def quit(self):
        print "Program End!"
        self.master.destroy()
