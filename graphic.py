#!/usr/bin/env python

from Tkinter import *
from game import Info

class Grid:
    def __init__(self, graphInfo):
        self.wid = graphInfo.width
        self.hei = graphInfo.height
        self.data = [[0] * self.hei for _ in range(self.wid)]
        self.initDataFromInfo(graphInfo)

    def initDataFromInfo(self, graphInfo):
        for x in range(self.wid):
            for y in range(self.hei):
                dataType = graphInfo.data[x][y][0]
                if dataType == Info.FIELD or dataType == Info.CROSSROAD:
                    self.data[x][y] = 0
                elif dataType == Info.INTERSECTION:
                    self.data[x][y] = 2
                elif dataType == Info.ROAD:
                    self.data[x][y] = 1

class Graphic():
    def __init__(self, grid, carList, gridsize=10):
        self.master = Tk()
        self.master.title("Traffic Flow Optimization")
        self.frame1 = Frame(self.master)
        self.frame1.pack()
        self.frame2 = Frame(self.master)
        self.frame2.pack()

        # real grid size = 10
        # map editor grid size = 10 x 2
        self.gridSize = gridsize
        self.width = grid.wid * gridsize
        self.height = grid.hei * gridsize
        self.cars = carList

        self.canvas = Canvas(self.frame1, width=self.width, height=self.height)
        self.canvas.pack()
        self.drawRoadAndBuilding(grid)

        self.quitButton = Button(self.frame2, text="Quit", command=self.quit)
        self.quitButton.grid(row=0, column=0)

        self.carItem = []
        self.frame1.after(100, self.drawCars)

    def run(self):
        self.master.mainloop()

    def drawRoadAndBuilding(self, grid):
        gridsize = self.gridSize
        for x in range(grid.wid):
            for y in range(grid.hei):
                pos_x = x * gridsize
                pos_y = y * gridsize
                if grid.data[x][y] == 0:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#eee", width=0)
                elif grid.data[x][y] == 2:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#393", width=0)
                else:
                    self.canvas.create_rectangle(pos_x, pos_y, pos_x+gridsize, pos_y+gridsize, fill="#333", width=0)

    def drawCars(self):
        gridsize = self.gridSize
        for item in self.carItem:
            self.canvas.delete(item)
        self.carItem = []
        for car in self.cars:
            x, y = car.pos
            pos_x = x * gridsize
            pos_y = y * gridsize
            self.carItem.append(self.canvas.create_oval(pos_x+1, pos_y+1, pos_x+gridsize-1, pos_y+gridsize-1, fill="#f96"))

        self.frame1.after(100, self.drawCars)

    def quit(self):
        print "Program End!"
        self.master.destroy()
