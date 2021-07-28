# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

import random
from AI import AI
from Action import Action

class MyAI( AI ):
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.rowDimension = colDimension
        self.colDimension = rowDimension
        
        self.lastMove = (startX, startY)  
        self.totalMines = totalMines
        
        self.freeSquares = []
        self.mines = []
        
        self.grid = Grid(colDimension, rowDimension)

        
    def getAction(self, number: int) -> "Action Object":  
        if number != -1:
            self.grid.setSquare(self.lastMove[0], self.lastMove[1], number)
        
        if (len(self.freeSquares) > 0):
            square = self.freeSquares.pop()
            self.lastMove = (square[0], square[1])
            return Action(AI.Action.UNCOVER, square[0], square[1])
        if (len(self.grid.getUnmarkedDict()) == 0):
            return Action(AI.Action.LEAVE)
        
        if (len(self.mines) > 0):
            square = self.mines.pop()
            self.grid.flagSquare(square[0], square[1])
            return Action(AI.Action.FLAG, square[0], square[1])
        if (len(self.grid.getFlaggedSet()) == self.totalMines):
            self.freeSquares = list(self.grid.getUnmarkedDict().keys())
        
        square = self.grid.findFree()
        if (square is not None):
            self.lastMove = (square[0], square[1])
            return Action(AI.Action.UNCOVER, square[0], square[1])
        
        li = self.grid.findMines()
        if (li is not None):
            square = li.pop()
            self.grid.flagSquare(square[0], square[1])
            for mine in li:
                self.mines.append(mine)
            return Action(AI.Action.FLAG, square[0], square[1])
        
        ###
        unmarkedDict = self.grid.getUnmarkedDict()
        flipped = dict([(value, key) for key, value in unmarkedDict.items()])
        
        li = list(flipped.keys())
        if (li) and (-1 in li):
            li.remove(-1)
        if (li):
            square = flipped[min(li)]
            self.lastMove = (square[0], square[1])
            return Action(AI.Action.UNCOVER, square[0], square[1])
        ###
        
        li = list(self.grid.getUnmarkedDict().keys())
        square = li[random.randint(0, len(li) - 1)]
        self.lastMove = (square[0], square[1])
        return Action(AI.Action.UNCOVER, square[0], square[1])
    
        
class Grid():
    def __init__(self, rowDimension, colDimension):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        
        self.markedDict = dict()
        self.unmarkedDict = dict()
        self.flaggedSet = set()
        
        for i in range(rowDimension):
            for j in range(colDimension):
                self.unmarkedDict[(i, j)] = -1
                
                
    def setSquare(self, x, y, num):
        if ((x, y) in self.unmarkedDict):
            del self.unmarkedDict[(x, y)]
            self.markedDict[(x, y)] = num - len(self.getFlaggedNeighbors(x, y))
            self.setProbability(x, y)
        
    
    def getMarkedDict(self):
        return self.markedDict
            
            
    def getUnmarkedDict(self):
        return self.unmarkedDict
    
    
    def getFlaggedSet(self):
        return list(self.flaggedSet)
    
    
    def setProbability(self, x, y):
        li = self.getUnmarkedNeighbors(x, y)
        prob = 1 if not li else self.markedDict[(x, y)] / len(li)
        for square in li:
            i = square[0]
            j = square[1]
            if (self.unmarkedDict[(i, j)] == -1):
                self.unmarkedDict[(i, j)] = prob
            else:
#                 self.unmarkedDict[(i, j)] = (self.unmarkedDict[(i, j)] + prob) / 1.85
                self.unmarkedDict[(i, j)] = self.unmarkedDict[(i, j)] + prob - (max(self.unmarkedDict[(i, j)], prob) / 1.3)
#                 self.unmarkedDict[(i, j)] = self.unmarkedDict[(i, j)] + prob - (min(self.unmarkedDict[(i, j)], prob) / 2)
    
    
    def findMines(self):
        for key, num in self.markedDict.items():
            li = self.getUnmarkedNeighbors(key[0], key[1])
            if (num != 0) and (num == len(li)):
                return li
        return None
    
       
    def flagSquare(self, x, y):
        del self.unmarkedDict[(x, y)]
        self.flaggedSet.add((x, y))
        self.decrementNeighbors(x, y)
    
    
    def findFree(self):
        for key, num in self.markedDict.items():
            i = key[0]
            j = key[1]
            if (0 == num):
                if ((i - 1, j - 1) in self.unmarkedDict):
                    return (i - 1, j - 1)
                elif ((i - 1, j) in self.unmarkedDict):
                    return (i - 1, j)
                elif ((i - 1, j + 1) in self.unmarkedDict):
                    return (i - 1, j + 1)
                elif ((i, j - 1) in self.unmarkedDict):
                    return (i, j - 1)
                elif ((i, j + 1) in self.unmarkedDict):
                    return (i, j + 1)
                elif ((i + 1, j - 1) in self.unmarkedDict):
                    return (i + 1, j - 1)
                elif ((i + 1, j) in self.unmarkedDict):
                    return (i + 1, j)
                elif ((i + 1, j + 1) in self.unmarkedDict):
                    return (i + 1, j + 1)  
        return None
        
    
    def decrementNeighbors(self, x, y):
        if ((x - 1, y - 1) in self.markedDict):
            self.markedDict[(x - 1, y - 1)] -= 1
#             self.setProbability(x - 1, y - 1)
        if ((x - 1, y) in self.markedDict):
            self.markedDict[(x - 1, y)] -= 1
#             self.setProbability(x - 1, y)
        if ((x - 1, y + 1) in self.markedDict):
            self.markedDict[(x - 1, y + 1)] -= 1
#             self.setProbability(x - 1, y + 1)
        if ((x, y - 1) in self.markedDict):
            self.markedDict[(x, y - 1)] -= 1
#             self.setProbability(x, y - 1)
        if ((x, y + 1) in self.markedDict):
            self.markedDict[(x, y + 1)] -= 1
#             self.setProbability(x, y + 1)
        if ((x + 1, y - 1) in self.markedDict):
            self.markedDict[(x + 1, y - 1)] -= 1
#             self.setProbability(x + 1, y - 1) 
        if ((x + 1, y) in self.markedDict):
            self.markedDict[(x + 1, y)] -= 1
#             self.setProbability(x + 1, y)
        if ((x + 1, y + 1) in self.markedDict):
            self.markedDict[(x + 1, y + 1)] -= 1
#             self.setProbability(x + 1, y + 1)
        
    
    def getUnmarkedNeighbors(self, x, y):
        li = []
        
        if ((x - 1, y - 1) in self.unmarkedDict):
            li.append((x - 1, y - 1))
        if ((x - 1, y) in self.unmarkedDict):
            li.append((x - 1, y))
        if ((x - 1, y + 1) in self.unmarkedDict):
            li.append((x - 1, y + 1))
        if ((x, y - 1) in self.unmarkedDict):
            li.append((x, y - 1))
        if ((x, y + 1) in self.unmarkedDict):
            li.append((x, y + 1))
        if ((x + 1, y - 1) in self.unmarkedDict):
            li.append((x + 1, y - 1))
        if ((x + 1, y) in self.unmarkedDict):
            li.append((x + 1, y))
        if ((x + 1, y + 1) in self.unmarkedDict):
            li.append((x + 1, y + 1))
        
        return li
    
    
    def getFlaggedNeighbors(self, x, y):
        li = []
        
        if ((x - 1, y - 1) in self.flaggedSet):
            li.append((x - 1, y - 1))
        if ((x - 1, y) in self.flaggedSet):
            li.append((x - 1, y))
        if ((x - 1, y + 1) in self.flaggedSet):
            li.append((x - 1, y + 1))
        if ((x, y - 1) in self.flaggedSet):
            li.append((x, y - 1))
        if ((x, y + 1) in self.flaggedSet):
            li.append((x, y + 1))
        if ((x + 1, y - 1) in self.flaggedSet):
            li.append((x + 1, y - 1))
        if ((x + 1, y) in self.flaggedSet):
            li.append((x + 1, y))
        if ((x + 1, y + 1) in self.flaggedSet):
            li.append((x + 1, y + 1))
        
        return li
