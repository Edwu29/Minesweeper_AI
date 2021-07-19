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
        if (len(self.grid.getUnmarkedSet()) == 0):
            return Action(AI.Action.LEAVE)
        
        if (len(self.mines) > 0):
            square = self.mines.pop()
            self.grid.flagSquare(square[0], square[1])
            return Action(AI.Action.FLAG, square[0], square[1])
        if (len(self.grid.getFlaggedSet()) == self.totalMines):
            self.freeSquares = self.grid.getUnmarkedSet()
        
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
        
        li = self.grid.getUnmarkedSet();
        square = li[random.randint(0, len(li) - 1)]
        self.lastMove = (square[0], square[1])
        return Action(AI.Action.UNCOVER, square[0], square[1])
    
        
class Grid():
    def __init__(self, rowDimension, colDimension):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        
        self.markedDict = dict()
        self.unmarkedSet = set()
        self.flaggedSet = set()
        
        for i in range(rowDimension):
            for j in range(colDimension):
                self.unmarkedSet.add((i, j))
                
                
    def setSquare(self, x, y, num):
        if ((x, y) in self.unmarkedSet):
            self.unmarkedSet.remove((x, y))
            self.markedDict[(x, y)] = num - len(self.getFlaggedNeighbors(x, y))
             
            
    def getUnmarkedSet(self):
        return list(self.unmarkedSet)
    
    
    def getFlaggedSet(self):
        return list(self.flaggedSet)
    
    
    def findMines(self):
        for key, num in self.markedDict.items():
            li = self.getUnmarkedNeighbors(key[0], key[1])
            if (num != 0) and (num == len(li)):
                return li
        return None

       
    def flagSquare(self, x, y):
        self.unmarkedSet.remove((x, y))
        self.flaggedSet.add((x, y))
        self.decrementNeighbors(x, y)
    
    
    def findFree(self):
        for key, num in self.markedDict.items():
            i = key[0]
            j = key[1]
            if (0 == num):
                if ((i - 1, j - 1) in self.unmarkedSet):
                    return (i - 1, j - 1)
                elif ((i - 1, j) in self.unmarkedSet):
                    return (i - 1, j)
                elif ((i - 1, j + 1) in self.unmarkedSet):
                    return (i - 1, j + 1)
                elif ((i, j - 1) in self.unmarkedSet):
                    return (i, j - 1)
                elif ((i, j + 1) in self.unmarkedSet):
                    return (i, j + 1)
                elif ((i + 1, j - 1) in self.unmarkedSet):
                    return (i + 1, j - 1)
                elif ((i + 1, j) in self.unmarkedSet):
                    return (i + 1, j)
                elif ((i + 1, j + 1) in self.unmarkedSet):
                    return (i + 1, j + 1)  
        return None
        
    
    def decrementNeighbors(self, x, y):
        if ((x - 1, y - 1) in self.markedDict):
            self.markedDict[(x - 1, y - 1)] -= 1
        if ((x - 1, y) in self.markedDict):
            self.markedDict[(x - 1, y)] -= 1
        if ((x - 1, y + 1) in self.markedDict):
            self.markedDict[(x - 1, y + 1)] -= 1
        if ((x, y - 1) in self.markedDict):
            self.markedDict[(x, y - 1)] -= 1
        if ((x, y + 1) in self.markedDict):
            self.markedDict[(x, y + 1)] -= 1
        if ((x + 1, y - 1) in self.markedDict):
            self.markedDict[(x + 1, y - 1)] -= 1
        if ((x + 1, y) in self.markedDict):
            self.markedDict[(x + 1, y)] -= 1
        if ((x + 1, y + 1) in self.markedDict):
            self.markedDict[(x + 1, y + 1)] -= 1
        
    
    def getUnmarkedNeighbors(self, x, y):
        li = []
        
        if ((x - 1, y - 1) in self.unmarkedSet):
            li.append((x - 1, y - 1))
        if ((x - 1, y) in self.unmarkedSet):
            li.append((x - 1, y))
        if ((x - 1, y + 1) in self.unmarkedSet):
            li.append((x - 1, y + 1))
        if ((x, y - 1) in self.unmarkedSet):
            li.append((x, y - 1))
        if ((x, y + 1) in self.unmarkedSet):
            li.append((x, y + 1))
        if ((x + 1, y - 1) in self.unmarkedSet):
            li.append((x + 1, y - 1))
        if ((x + 1, y) in self.unmarkedSet):
            li.append((x + 1, y))
        if ((x + 1, y + 1) in self.unmarkedSet):
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
