#!/usr/bin/env python

from Tkinter import *
from random import randint

class App:
    def __init__(self, master):
        self.master = master

        self.frame1 = Frame(master)
        self.frame1.pack()
        self.frame2 = Frame(master)
        self.frame2.pack()

        # real grid size = 10
        # map editor grid size = 10 x 2
        self.gridSize = 20
        self.WID = 400
        self.HEI = 300
        self.vGrid = self.HEI / self.gridSize
        self.hGrid = self.WID / self.gridSize

        self.canvas = Canvas(self.frame1, width=self.WID, height=self.HEI)
        self.canvas.bind("<B1-Motion>", self.changeGridColor)
        self.canvas.bind("<Button-1>", self.changeGridColor)
        self.canvas.pack()

        self.grids = [[0 for __ in range(self.hGrid)] for _ in range(self.vGrid)]
        self.drawGrid()

        self.colorToDraw = "#333"
        self.toggleButton = Button(self.frame2, text="Toggle", command=self.toggleColor)
        self.toggleButton.grid(row=0, column=0)

        self.saveButton = Button(self.frame2, text="Save", command=self.saveGrid)
        self.saveButton.grid(row=0, column=1)

    def drawGrid(self):
        gLen = self.gridSize
        for i in range(self.vGrid):
            y = i * gLen
            for j in range(self.hGrid):
                x = j * gLen
                self.grids[i][j] = self.canvas.create_rectangle(x, y, x+gLen, y+gLen, fill="#efefef")

    def toggleColor(self):
        if self.colorToDraw == "#333":
            self.colorToDraw = "#efefef"
        else:
            self.colorToDraw = "#333"

    def changeGridColor(self, event):
        # print "Click at", event.x, event.y
        gLen = self.gridSize
        x = int(event.x / gLen)
        y = int(event.y / gLen)
        self.canvas.itemconfig(self.grids[y][x], fill=self.colorToDraw)

    def countNeighbors(self, stateGrids, i, j):
        count = 0
        for pos in [(i-1,j), (i,j-1), (i+1,j), (i,j+1)]:
            if pos[0] >= 0 and pos[0] <= len(stateGrids) and pos[1] >= 0 and pos[1] <= len(stateGrids[0]):
                if stateGrids[pos[0]][pos[1]] != 0:
                    count += 1
        return count

    def saveGrid(self):
        stateGrids = [[0 for i in range(self.hGrid)] for j in range(self.vGrid)]
        realGrids = [[0 for i in range(self.hGrid * 2)] for j in range(self.vGrid * 2)]

        for i in range(self.vGrid):
            for j in range(self.hGrid):
                fillColor = self.canvas.itemcget(self.grids[i][j], "fill")
                if fillColor == "#333":
                    stateGrids[i][j] = 1

        for i in range(self.vGrid):
            for j in range(self.hGrid):
                if stateGrids[i][j] == 1:
                    count = self.countNeighbors(stateGrids, i, j)
                    if count >= 3:
                        stateGrids[i][j] = 3

                realGrids[i*2][j*2] = stateGrids[i][j]
                realGrids[i*2+1][j*2] = stateGrids[i][j]
                realGrids[i*2][j*2+1] = stateGrids[i][j]
                realGrids[i*2+1][j*2+1] = stateGrids[i][j]

        for i in range(self.vGrid * 2):
            for j in range(self.hGrid * 2):
                if realGrids[i][j] == 0:
                    print "x",
                elif realGrids[i][j] == 1 or realGrids[i][j] == 2:
                    print "1",
                else:
                    print "C",
            print ""

        self.master.destroy()

if __name__ == '__main__':
    root = Tk()
    root.title("test.py")
    app = App(root)
    root.mainloop()
