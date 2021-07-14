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

from AI import AI
from Action import Action

import numpy as np

class MyAI( AI ):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.numUncovered = 0
        self.numFlagged = 0
        
        #create board
        self.board = np.full((rowDimension, colDimension), -1) #label, effective label, type(covered, uncovered, flagged, unflagged)
        self.efflabel = np.full((rowDimension, colDimension), -1)
        self.type = np.full((rowDimension, colDimension), "unmarked")
        #UNCOVER the startX and startY
        self.currentAction = Action(AI.Action.UNCOVER, startX, startY)
        
        
    def getAction(self, number: int) -> "Action Object":
        #successful goal state
        if (self.rowDimension*self.colDimension) - self.totalMines == self.numUncovered:
            return Action(AI.Action.LEAVE)
        
        x=self.currentAction.getX()
        y=self.currentAction.getY()
        # if the previous action was an UNCOVER action, update the board
        if number != -1:
            self.type[x, y] = "uncovered"
            self.board[x, y] = number
        
            #effectivelabel(x) = label(x) - numMarkedNeighbors(x)
            numMarkedNeighbors = self.getNumMarkedNeighbors(x, y)
            self.efflabel[x, y] = self.board[x, y] - numMarkedNeighbors
            
            #print(x, y)
            #print(self.efflabel[x, y])
            #print(self.getNumUnmarkedNeighbors(x, y))
            # check if self.efflabel[x, y] (effective label) == 0, we can uncover the unflagged(unmarked) tiles.
            if self.efflabel[x, y] == 0:
                # check surrounding
                return self.uncoverUnmarkedTile(x, y)
                

            # if self.efflabel[x, y] (effective label) == numUnmarkedNeighbors, then all of them must be mines, we can flag them,
            # this reduces the effective label of other tiles within the window.
            if self.efflabel[x, y] == self.getNumUnmarkedNeighbors(x, y):
                return self.markAndDecrementNeighbors(x, y)
    
    def getNumMarkedNeighbors(self, x: int, y: int):
        numMarkedNeighbors = 0
        
        try: 
            if self.type[x - 1, y + 1] == "marked": numMarkedNeighbors +=1
        except: pass
        
        try: 
            if self.type[x, y + 1] == "marked": numMarkedNeighbors +=1
        except: pass
        
        try: 
            if self.type[x + 1, y + 1] == "marked": numMarkedNeighbors +=1  
        except: pass
        
        try: 
            if self.type[x + 1, y] == "marked": numMarkedNeighbors +=1  
        except: pass
        
        try: 
            if self.type[x + 1, y - 1] == "marked": numMarkedNeighbors +=1 
        except: pass
        
        try: 
            if self.type[x, y - 1] == "marked": numMarkedNeighbors +=1 
        except: pass
        
        try: 
            if self.type[x - 1, y - 1] == "marked": numMarkedNeighbors +=1
        except: pass
        
        try: 
            if self.type[x - 1, y] == "marked": numMarkedNeighbors +=1 
        except: pass
        
        return numMarkedNeighbors
    
    
    def getNumUnmarkedNeighbors(self, x: int, y: int):
        unmarkedTiles = 0
        
        try: 
            if self.type[x - 1, y + 1] == "unmarked": unmarkedTiles +=1
        except: pass
        
        try: 
            if self.type[x, y + 1] == "unmarked": unmarkedTiles +=1
        except: pass
        
        try: 
            if self.type[x + 1, y + 1] == "unmarked": unmarkedTiles +=1  
        except: pass
        
        try: 
            if self.type[x + 1, y] == "unmarked": unmarkedTiles +=1  
        except: pass
        
        try: 
            if self.type[x + 1, y - 1] == "unmarked": unmarkedTiles +=1 
        except: pass
        
        try: 
            if self.type[x, y - 1] == "unmarked": unmarkedTiles +=1 
        except: pass
        
        try: 
            if self.type[x - 1, y - 1] == "unmarked": unmarkedTiles +=1
        except: pass
        
        try: 
            if self.type[x - 1, y] == "unmarked": unmarkedTiles +=1 
        except: pass
        
        return unmarkedTiles
    
    def getNumUncoveredTiles(self, x: int, y: int):
        uncoveredTiles = 0
        
        try: 
            if self.type[x - 1, y + 1] == "uncovered": uncoveredTiles +=1
        except: pass
        
        try: 
            if self.type[x, y + 1] == "uncovered": uncoveredTiles +=1
        except: pass
        
        try: 
            if self.type[x + 1, y + 1] == "uncovered": uncoveredTiles +=1  
        except: pass
        
        try: 
            if self.type[x + 1, y] == "uncovered": uncoveredTiles +=1  
        except: pass
        
        try: 
            if self.type[x + 1, y - 1] == "uncovered": uncoveredTiles +=1 
        except: pass
        
        try: 
            if self.type[x, y - 1] == "uncovered": uncoveredTiles +=1 
        except: pass
        
        try: 
            if self.type[x - 1, y - 1] == "uncovered": uncoveredTiles +=1
        except: pass
        
        try: 
            if self.type[x - 1, y] == "uncovered": uncoveredTiles +=1 
        except: pass
        
        return uncoveredTiles
    
    def getCoordOfUnmarkedTile(self, x: int, y: int):
        pass
    
    def updateSurroundings(self, x, y):
        self.efflabel[x - 1, y + 1]-=1
        self.efflabel[x, y + 1]-=1
        self.efflabel[x + 1, y + 1]-=1
        self.efflabel[x + 1, y]-=1
        self.efflabel[x + 1, y - 1]-=1
        self.efflabel[x, y - 1]-=1
        self.efflabel[x - 1, y - 1]-=1
        self.efflabel[x - 1, y]-=1
        return
    def uncoverUnmarkedTile(self, x: int, y: int):
        # top
        if ((x - 1) >= 0):
            # top left
            if ((y - 1) >= 0) and (self.type[x - 1, y - 1] == "unmarked"):
                self.type[x - 1, y - 1] = "uncovered"
                self.currentAction = Action(AI.Action.UNCOVER, x - 1, y - 1)
                return self.currentAction
            # top center
            elif (self.type[x - 1, y] == "unmarked"):
                self.type[x - 1, y] = "uncovered"
                self.currentAction = Action(AI.Action.UNCOVER, x - 1, y)
                return self.currentAction
            # top right
            elif ((y + 1) < self.colDimension) and (self.type[x - 1, y + 1] == "unmarked"):
                self.type[x - 1, y + 1] = "uncovered"
                self.currentAction = Action(AI.Action.UNCOVER, x - 1, y + 1)
                return self.currentAction
        # middle left
        if ((y - 1) >= 0) and (self.type[x, y - 1] == "unmarked"):
            self.type[x, y - 1] = "uncovered"
            self.currentAction = Action(AI.Action.UNCOVER, x, y - 1)
            return self.currentAction
        # middle right
        if ((y + 1) < self.colDimension) and (self.type[x, y + 1] == "unmarked"):
            self.type[x, y + 1] = "uncovered"
            self.currentAction = Action(AI.Action.UNCOVER, x, y + 1)
            return self.currentAction
        # bottom row
        if ((x + 1) < self.rowDimension):
            # bottom left
            if ((y - 1) >= 0) and (self.type[x + 1, y - 1] == "unmarked"):
                self.type[x + 1, y - 1] = "uncovered"
                self.currentAction = Action(AI.Action.UNCOVER, x + 1, y - 1)
                return self.currentAction
            # bottom center
            elif (self.type[x + 1, y] == "unmarked"):
                self.type[x + 1, y] = "uncovered"
                self.currentAction = Action(AI.Action.UNCOVER, x + 1, y)
                return self.currentAction
            # bottom right
            elif ((y + 1) < self.colDimension) and (self.type[x + 1, y + 1] == "unmarked"):
                self.type[x + 1, y + 1] = "uncovered"
                self.currentAction = Action(AI.Action.UNCOVER, x + 1, y + 1)
                return self.currentAction 
            
    #Mark the tile and decrement its neighbors effective label by 1
    def markAndDecrementNeighbors(self, x: int, y: int):
        if ((x - 1) >= 0):
            # top left
            if ((y - 1) >= 0) and (self.type[x - 1, y - 1] == "unmarked"):
                self.type[x - 1, y - 1] = "marked"
                self.updateSurroundings(x - 1, y - 1)
                self.currentAction = Action(AI.Action.FLAG, x - 1, y - 1)
                return self.currentAction
            # top center
            elif (self.type[x - 1, y] == "unmarked"):
                self.type[x - 1, y] = "marked"
                self.updateSurroundings(x - 1, y)
                self.currentAction = Action(AI.Action.FLAG, x - 1, y)
                return self.currentAction
            # top right
            elif ((y + 1) < self.colDimension) and (self.type[x - 1, y + 1] == "unmarked"):
                self.type[x - 1, y + 1] = "marked"
                self.updateSurroundings(x - 1, y + 1)
                self.currentAction = Action(AI.Action.FLAG, x - 1, y + 1)
                return self.currentAction
        # middle left
        if ((y - 1) >= 0) and (self.type[x, y - 1] == "unmarked"):
            self.type[x, y - 1] = "marked"
            self.updateSurroundings(x, y - 1)
            self.currentAction = Action(AI.Action.FLAG, x, y - 1)
            return self.currentAction
        # middle right
        if ((y + 1) < self.colDimension) and (self.type[x, y + 1] == "unmarked"):
            self.type[x, y + 1] = "marked"
            self.updateSurroundings(x, y + 1)
            self.currentAction = Action(AI.Action.FLAG, x, y + 1)
            return self.currentAction
        # bottom row
        if ((x + 1) < self.rowDimension):
            # bottom left
            if ((y - 1) >= 0) and (self.type[x + 1, y - 1] == "unmarked"):
                self.type[x + 1, y - 1] = "marked"
                self.updateSurroundings(x + 1, y - 1)
                self.currentAction = Action(AI.Action.FLAG, x + 1, y - 1)
                return self.currentAction
            # bottom center
            elif (self.type[x + 1, y] == "unmarked"):
                self.type[x + 1, y] = "marked"
                self.updateSurroundings(x + 1, y)
                self.currentAction = Action(AI.Action.FLAG, x + 1, y)
                return self.currentAction
            # bottom right
            elif ((y + 1) < self.colDimension) and (self.type[x + 1, y + 1] == "unmarked"):
                self.type[x + 1, y + 1] = "marked"
                self.updateSurroundings(x + 1, y + 1)
                self.currentAction = Action(AI.Action.FLAG, x + 1, y + 1)
                return self.currentAction