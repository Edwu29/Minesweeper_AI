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
        self.__rowDimension = rowDimension
        self.__colDimension = colDimension
        self.__totalMines = totalMines
        self.__numUncovered = 0
        self.__numFlagged = 0
        
        #create board
        self.board = np.full((rowDimension, colDimension), -1) #label, effective label, type(uncovered, flagged, unflagged)
        self.efflabel = np.full((rowDimension, colDimension), -1)
        self.type = np.full((rowDimension, colDimension), "unflagged")
        #UNCOVER the startX and startY
        self.currentAction = Action(AI.Action.UNCOVER, startX, startY)
        
    def getAction(self, number: int) -> "Action Object":
        #successful goal state
        if (self.__rowDimension*self.__colDimension) - self.__totalMines == self.__numUncovered:
            return Action(AI.Action.LEAVE)
        
        
        x=self.currentAction.getX()
        y=self.currentAction.getY()
        # if the previous action was an UNCOVER action, update the board
        if number != -1:
            self.type[x, y] = "uncovered"
            self.board[x, y] = number
        
            #effectivelabel(x) = label(x) - numMarkedNeighbors(x)
            numMarkedNeighbors = getnumMarkedNeighbors(x, y)
            self.efflabel[x, y] = self.board[x, y] - numMarkedNeighbors
            
            # check if self.efflabel[x, y] (effective label) == 0, we can uncover the unflagged(unmarked) tiles.
            if self.efflabel[x, y] == 0:
                # check surrounding
                
                # top
                if ((x - 1) >= 0):
                    # top left
                    if ((y - 1) >= 0) and (self.type[x - 1, y - 1] == "unmarked"):
                        self.type[x - 1, y - 1] == "marked"
                        return Action(AI.Action.UNCOVER, x - 1, y - 1)
                    # top center
                    elif (self.type[x - 1, y] == "unmarked"):
                        self.type[x - 1, y] == "marked"
                        return Action(AI.Action.UNCOVER, x - 1, y)
                    # top right
                    elif ((y + 1) < self.colDimension) and (self.type[x - 1, y + 1] == "unmarked"):
                        self.type[x - 1, y + 1] == "marked"
                        return Action(AI.Action.UNCOVER, x - 1, y + 1)
                # middle left
                if ((y - 1) >= 0) and (self.type[x, y - 1] == "unmarked"):
                    self.type[x, y - 1] == "marked"
                    return Action(AI.Action.UNCOVER, x, y - 1)
                # middle right
                if ((y + 1) < self.colDimension) and (self.type[x, y + 1] == "unmarked"):
                    self.type[x, y + 1] == "marked"
                    return Action(AI.Action.UNCOVER, x, y + 1)
                # bottom row
                if ((x + 1) < self.rowDimension):
                    # bottom left
                    if ((y - 1) >= 0) and (self.type[x + 1, y - 1] == "unmarked"):
                        self.type[x + 1, y - 1] == "marked"
                        return Action(AI.Action.UNCOVER, x + 1, y - 1)
                    # bottom center
                    elif (self.type[x + 1, y] == "unmarked"):
                        self.type[x + 1, y] == "marked"
                        return Action(AI.Action.UNCOVER, x + 1, y)
                    # bottom right
                    elif ((y + 1) < self.colDimension) and (self.type[x + 1, y + 1] == "unmarked"):
                        self.type[x + 1, y + 1] == "marked"
                        return Action(AI.Action.UNCOVER, x + 1, y + 1)
            
            # if self.efflabel[x, y] (effective label) == numUnmarkedNeighbors, then all of them must be mines, we can flag them,
            # this reduces the effective label of other tiles within the window. 
            if self.efflabel[x, y] == getNumUnmarkedNeighbors(x, y):
                pass
            
            # if self.efflabel[x, y] (effective label) == numUnmarkedNeighbors, then all of them must be mines, we can flag them,
            # this reduces the effective label of other tiles within the window. 
            if self.efflabel[x, y] == getNumUnmarkedNeighbors(x, y):
                pass
    
    def getNumMarkedNeighbors(self, x: int, y: int):
        numMarkedNeighbors = 0
        
        try: if self.type[x - 1, y + 1] == "flagged": numMarkedNeighbors +=1
        except: pass
        
        try: if self.type[x, y + 1] == "flagged": numMarkedNeighbors +=1
        except: pass
        
        try: if self.type[x + 1, y + 1] == "flagged": numMarkedNeighbors +=1  
        except: pass
        
        try: if self.type[x + 1, y] == "flagged": numMarkedNeighbors +=1  
        except: pass
        
        try: if self.type[x + 1, y - 1] == "flagged": numMarkedNeighbors +=1 
        except: pass
        
        try: if self.type[x, y - 1] == "flagged": numMarkedNeighbors +=1 
        except: pass
        
        try: if self.type[x - 1, y - 1] == "flagged": numMarkedNeighbors +=1
        except: pass
        
        try: if self.type[x - 1, y] == "flagged": numMarkedNeighbors +=1 
        except: pass
        
        return numMarkedNeighbors
    def getnumUnmarkedNeighbors(self, x: int, y: int):
        return 9 - getnumMarkedNeighbors(x, y)
    
    def getCoordOfUnmarkedTile(self, x: int, y: int):
        pass
