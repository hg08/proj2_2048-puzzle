#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 21:58:34 2018

@author: huang
"""

import queue as Q
import math
import time
import random

from BaseAI_3 import BaseAI

# to determine the deepest search depth

max_depth = 4
size = 4

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
vecIndex = [UP, DOWN, LEFT, RIGHT] = range(4)

class PlayerAI(BaseAI):
    # grid, is similar to "state"
    def getMove(self, grid):
        
        global frontier,size
        
        # possible moves for MAX: moves[i] 
        moves = grid.getAvailableMoves()
        print('\nAvailable moves:',moves)
        # print(time.process_time())
        optimal_move = moves[0]
        return optimal_move
    
    def utility(grid):
        return 2.0 + random.uniform(0, 2)
    
    def maximize(self,grid):
        if not grid.canMove(dirs = vecIndex):
            return self.utility(grid)
    
        move(grid)
    