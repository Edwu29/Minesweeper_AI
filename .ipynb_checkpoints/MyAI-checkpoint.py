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
        self.board = np.full((rowDimension, colDimension), tuple(-1, -1, "uncovered")) #label, effective label, type(uncovered, flagged, unflagged)
        
        #UNCOVER the startX and startY
        self.currentAction = Action(AI.Action.UNCOVER, startX, startY)
        
    def getAction(self, number: int) -> "Action Object":
        #successful goal state
        if self.__rowDimension*self.__colDimension - self.__totalMines == self.__numUncovered:
            return Action(AI.Action.LEAVE)
        
        x=self.currentAction.getX()
        y=self.currentAction.getY()
        # if the previous action was an UNCOVER action, update the board
        if number != -1:
            self.board[x, y][0] = number
        
            #effectivelabel(x) = label(x) - numMarkedNeighbors(x)
            numMarkedNeighbors = getnumMarkedNeighbors()
            self.board[x, y][1] = self.board[x, y][0] - numMarkedNeighbors
        
    def getnumMarkedNeighbors(self, x: int, y: int):
        pass
        