# -*- coding: utf-8 -*-
import queue as Q
import math
import time

from BaseAI_3 import BaseAI
from Grid_3 import Grid

# to determine the deepest search depth

depth = 10
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
        frontier = Q.LifoQueue()
        (child, aaa) = Maxmize(grid, -10000, 10000)        
        for i in range(len(moves)):
            grid.move(moves[i])
            if grid.map == child.map:
                optimal_move = i
        return optimal_move
                       
        # I have to design a heuristic function to find the optimal move.
        #
        # Heuristic function allow me to approximate the true utility of a state
        # without doing a complete search.
        # h(grid) = grid.getMaxTile()
        
        # 2048-puzzle is a game with two players
        # Max: Player AI
        # Min: Computer AI
        
        # if h(grid) == 2048, then Min win!
        
        # S_0: The initial state of the class grid
        # Player(grid) = 0 or 1
        # Actions(grid) : returns a set of legal moves in a state
        
        # Utility(terminal_grid,player) : 1, 0, or 1/2
                   
# Maxmize
        
def mapping(grid):
    x = grid.map
    
        

def Maxmize(initial_state,alpha, beta):
    """
    For Max, to choose the largest utility among the children of initial_state.
    return: (maxChild, maxUtility)
    """
    global frontier, size
    # Declare the global variables
    #global cost_of_path,nodes_expanded,set_search_depth
    
    max_depth = 3
    # The stack
    frontier._put(initial_state)
    #frontier_map = set()

    # create a new set and a new LifoQueue: explored,explored_LifoQueue
    explored = set()
    explored_LifoQueue = Q.LifoQueue()
    explored_map = set()

    while frontier._qsize():
        state = frontier._get()
        #set_search_depth.add(state.cost)
        explored.add(state)
        explored_LifoQueue._put(state)
        li_state = []
        for i in range(size):
            for j in range(size):
                li_state.append(state.map[i][j])
        explored_map.add(tuple(li_state))
            
        for depth in range(10000):
            if test_terminal(state,depth):
                #the number of nodes expanded
                nodes_expanded = len(explored)-1
                return (, eva(state))

        (maxChild, maxUtility) = (None, -10000)
        for neighbor in state.expand_reverse():
            XXX,utility = Minimize(state,alpha,beta)
            
            if utility > maxUtility:
                (maxChild, maxUtility) = neighbor, utility
            if maxUtility > beta or maxUtility == beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility

    return (maxChild, maxUtility)            

# Maxmize
def Minimize(initial_state,alpha, beta):
    """
    For Min, to choose the minimum of utility of the children of initial_state.
    return (minChild, minUtility)
    """
    global frontier, size
    # Declare the global variables
    #global cost_of_path,nodes_expanded,
    set_search_depth = set()

    # The stack
    frontier._put(initial_state)
    frontier_map = set()

    # create a new set and a new LifoQueue: explored,explored_LifoQueue
    explored = set()
    explored_LifoQueue = Q.LifoQueue()
    explored_map = set()

    while frontier._qsize():
        state = frontier._get()
        #set_search_depth.add(state.cost)
        explored.add(state)
        explored_LifoQueue._put(state)
        li_state = []
        for i in range(size):
            for j in range(size):
                li_state.append(state.map[i][j])
        explored_map.add(tuple(li_state))
            
        for depth in range(10000):
            if test_terminal(state,depth):
                #the number of nodes expanded
                nodes_expanded = len(explored)-1
                return (None, eva(state))
        
        (minChild, minUtility) = (None, 10000)
        for neighbor in state.expand_reverse():
            XXX,utility = Maxmize(state,alpha,beta)
            
            if utility < minUtility:
                (minChild, minUtility) = (neighbor, utility)
            
            if minUtility < alpha or minUtility == alpha:
                break
            
            if minUtility < beta:
                beta = minUtility

    return (minChild, minUtility)     
    
def h_minimax(puzzle_grid,depth):
    pass
    
# check if it should be cut off
def test_terminal(puzzle_state,depth):
    """test the state is the goal state or not"""
    #if puzzle_state.cost == depth:
    if not type(puzzle_state).__name__ == "dict":
        return True
    else:
        return False

def test_goal(puzzle_state):
    """test the grid is the goal state or not"""
    if max(20, 30, 1024) == 2048:
        return True
    else:
        return False
    
def smoothness(puzzle_grid):
    pass

def monotonicity(puzzle_grid):
    pass
    
def eva(puzzle_grid):
    emptycells = len(puzzle_grid.getAvailableCells())   
    
    w_smooth = 0.1
    w_mono = 1.0
    w_empty = 2.7
    w_max = 1.0
      
    #result = smoothness(puzzle_grid) * w_smooth + monotonicity(puzzle_grid) * w_mono \
    #          + math.log(empthcells) * w_empty + puzzle_grid.getMaxTile() * w_max
    result = math.log(emptycells+1) * w_empty + puzzle_grid.getMaxTile() * w_max
    
    return result

class PuzzleState(Grid):
    """The Class PuzzleState"""
    def __init__(self, size=4, parent=None, cost=0):
        Grid.__init__(self, size = 4)
        self.cost = cost
        self.parent = parent
        self.children = []
        
        """
        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break
        """
    # expand the node
    def expand_reverse(self):
        """expand the node. Here we add child nodes in order of reverse-UDLR."""
        if len(self.children) == 0:
            right_child = self.move(self,RIGHT)

            if right_child is not None:
                self.children.append(right_child)
                right_child.cost = self.cost + 1
                
            left_child = self.move(self,LEFT)

            if left_child is not None:
                self.children.append(left_child)
            down_child = self.move(self,DOWN)

            if down_child is not None:
                self.children.append(down_child)
            up_child = self.move(self,UP)

            if up_child is not None:
                self.children.append(up_child)
        return self.children