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

from collections import defaultdict
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
            self.lastMove = (square[0], square[1])
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
            self.lastMove = (square[0], square[1])
            return Action(AI.Action.FLAG, square[0], square[1])
        
    #model checking logic begin
        square = self.lastMove
        #getting covered frontier
        self.grid.getFrontier(square[0], square[1])
        coveredFrontier = self.grid.getCoveredFrontierSet()
        #getting uncovered frontier
        uncoveredFrontier = self.grid.getUncoveredFrontierSet()
        
        #assigning 1 and 0s for each value in coveredFrontier
        numOfBits = len(coveredFrontier)
        option = "0" + str(numOfBits) + "b"
        
        count = defaultdict(int)
        numOfModels = 0
        for i in range (pow(2, numOfBits)): #enumerating each assignment.
            bitRepresentation = format(i, option)
            #assign each c in coveredFrontier a bit from bitRepresentation
            assignments = {} #stores tiles as keys and the value as the assignment. Ex: key: (2, 3), value: 1 or key: (4, 8),
                                                                                                                   #value: 0
            for i, c in enumerate(coveredFrontier):
                assignments[c] = bitRepresentation[i]
                
            if self.isAssignmentsConsistent(assignments, uncoveredFrontier) == True: #if assignment is consistent
                #count the 0s and 1s for each tile.
                #print("it goes here!!!!!")
                numOfModels +=1
                for square in assignments.keys():
                    if assignments[square] == 1:
                        count[square]+=1
                
         #now we have a "count" dictionary. Each key represents a tile and the value is the number of times a model contains 1 in
                                                                                                                        #that tile
        for element in count.keys():
            if count[element]/numOfModels == 0:
                self.freeSquares.append(element)
            if count[element]/numOfModels == 1:
                self.mines.append(element)
                
            
        if (len(self.freeSquares) > 0):
            square = self.freeSquares.pop()
            self.lastMove = (square[0], square[1])
            return Action(AI.Action.UNCOVER, square[0], square[1])
        
        if (len(self.mines) > 0):
            square = self.mines.pop()
            self.grid.flagSquare(square[0], square[1])
            self.lastMove = (square[0], square[1])
            return Action(AI.Action.FLAG, square[0], square[1])
    #model checking logic end
    
    
    
    #if all else fails, guess
        #print("guessing here!!")
        li = self.grid.getUnmarkedSet();
        square = li[random.randint(0, len(li) - 1)]
        self.lastMove = (square[0], square[1])
        return Action(AI.Action.UNCOVER, square[0], square[1])
    
    
    def isAssignmentsConsistent(self, assignments, uncoveredFrontier):
        #for each uncoveredFrontier, check if their effective label is satisfied. Adding the covered neighbors should be equal to the EF label
        for u in uncoveredFrontier:
            effLabel = self.grid.markedDict[u]
            coveredNeighbors = self.grid.getUnmarkedNeighbors(u[0], u[1])
            
            count = 0
            for c in coveredNeighbors:
                if c in assignments:
                    count+=1
            
            if count != effLabel:
                return False
        
        return True
        
        
class Grid():
    def __init__(self, rowDimension, colDimension):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        
        self.markedDict = dict()
        self.unmarkedSet = set()
        self.flaggedSet = set()
        
        self.coveredFrontier = set()
        self.uncoveredFrontier = set()
        
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
    
    def getUncoveredFrontierSet(self):
        return list(self.uncoveredFrontier)
    
    def getCoveredFrontierSet(self):
        return list(self.coveredFrontier)
    
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
        
        if ((x - 1, y - 1) in self.unmarkedSet and (x - 1, y - 1) not in self.flaggedSet):
            li.append((x - 1, y - 1))
        if ((x - 1, y) in self.unmarkedSet and (x - 1, y) not in self.flaggedSet):
            li.append((x - 1, y))
        if ((x - 1, y + 1) in self.unmarkedSet and (x - 1, y + 1) not in self.flaggedSet):
            li.append((x - 1, y + 1))
        if ((x, y - 1) in self.unmarkedSet and (x, y - 1) not in self.flaggedSet):
            li.append((x, y - 1))
        if ((x, y + 1) in self.unmarkedSet and (x, y + 1) not in self.flaggedSet):
            li.append((x, y + 1))
        if ((x + 1, y - 1) in self.unmarkedSet and (x + 1, y - 1) not in self.flaggedSet):
            li.append((x + 1, y - 1))
        if ((x + 1, y) in self.unmarkedSet and (x + 1, y) not in self.flaggedSet):
            li.append((x + 1, y))
        if ((x + 1, y + 1) in self.unmarkedSet and (x + 1, y + 1) not in self.flaggedSet):
            li.append((x + 1, y + 1))
        
        return li
    
    def getMarkedNeighbors(self, x, y):
        li = []
        
        if ((x - 1, y - 1) in self.markedDict):
            li.append((x - 1, y - 1))
        if ((x - 1, y) in self.markedDict):
            li.append((x - 1, y))
        if ((x - 1, y + 1) in self.markedDict):
            li.append((x - 1, y + 1))
        if ((x, y - 1) in self.markedDict):
            li.append((x, y - 1))
        if ((x, y + 1) in self.markedDict):
            li.append((x, y + 1))
        if ((x + 1, y - 1) in self.markedDict):
            li.append((x + 1, y - 1))
        if ((x + 1, y) in self.markedDict):
            li.append((x + 1, y))
        if ((x + 1, y + 1) in self.markedDict):
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
    def getFrontier(self, x, y):
        #assuming the first x and y are uncovered frontier
        if ((x, y) in self.markedDict):
            self.uncoveredFrontier.add((x, y))
            self.getCoveredFrontier([(x, y)]) # this is a recursive call
            
        elif((x, y) in self.unmarkedSet):
            self.coveredFrontier.add((x, y))
            self.getUncoveredFrontier([(x, y)]) # this is a recursive call
        
    def getCoveredFrontier(self, uncovered):
        li = []
        #print("uncovered" + str(uncovered))
        
        if uncovered == []:
            return None
        
        for square in uncovered:
            x = square[0]
            y = square[1]
            arr = self.getUnmarkedNeighbors(x, y)
            li = [x for x in arr if x not in self.coveredFrontier]
            
        self.coveredFrontier.update(li)
        self.getUncoveredFrontier(list(li)) #kinda like recursive call
        
    def getUncoveredFrontier(self, covered):
        li = []
        #print("covered" + str(covered))
        if covered == []:
            return None
        
        for square in covered:
            x = square[0]
            y = square[1]
            
            arr = self.getMarkedNeighbors(x, y)
            li = [x for x in arr if x not in self.uncoveredFrontier]
        
        self.uncoveredFrontier.update(li)
        self.getCoveredFrontier(list(li))