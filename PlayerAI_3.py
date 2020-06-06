#===========
#The modules
#===========
from BaseAI_3 import BaseAI
from Grid_3 import *
import time

#=============================
#The def of the class PlayerAI
#=============================
class PlayerAI(BaseAI):
    #The main function: to move in one direction
	def getMove(self, grid):
		moves = grid.getAvailableMoves()
		maxUtility = -float("inf")
		nextMove = -1

		for move in moves:
			child = getChild(grid, move)

			utility = Decision(grid=child, max=False)

			if utility >= maxUtility:
				maxUtility = utility
				nextMove = move

		return nextMove

#========================================
#Functions used in the function getMove()
#========================================
#Gets the Child of a node in a particular direction
def getChild(grid, dir):
	grid_cp = grid.clone()
	grid_cp.move(dir)
	return grid_cp

#Gets all Children of a node
def children(grid):
	children = []
	for move in grid.getAvailableMoves():
		children.append(getChild(grid, move))
	return children

#Check if a node is a terminal
def terminal(grid):
	return not grid.canMove()

#Evaluates the heuristic. The heuristic includes three parts
def Eval(grid):
    score = 2.5*Eval_1(grid) + 63*Eval_2(grid) + Eval_3(grid)
    return score

#Part 1: To get the Max Value of a grid
def Eval_1(grid):
    if terminal(grid):
        return -float('inf')

    maxValue = grid.getMaxTile()
    score = maxValue
    return score

#Part 2: To claculate the utility related to the number of available cells
def Eval_2(grid):
    if terminal(grid):
        return -float('inf')

    score = numOfAvailableCells(grid)
    return score

#Part 3: A standard model for the cells values' distribution
def Eval_3(grid):
	if terminal(grid):
		return -float('inf')

	models = [[[ 3,  2,  1,  0],
               [ 2,  1,  0, -1],
               [ 1,  0, -1, -2],
               [ 0, -1, -2, -3]],
			  [[ 0, -1, -2, -3],[ 1,  0, -1, -2],[ 2,  1,  0, -1],[ 3, 2,  1, 0 ]],
			  [[ 0,  1,  2,  3],[-1,  0,  1,  2],[-2, -1,  0,  1],[-3, -2, -1, 0]],
			  [[-3, -2, -1,  0],[-2, -1,  0,  1],[-1,  0,  1,  2],[ 0,  1,  2,  3]]]
	values = [0,0,0,0]
	for i in range(4):
		for x in range(4):
			for y in range(4):
				values[i] += models[i][x][y]*grid.map[x][y]

	return max(values)

# To calculation the number of available cells
def numOfAvailableCells(grid):
    num = len(grid.getAvailableCells())
    return num

#=====================================
#The Minmax algorithm with a-b pruning
#=====================================
#Returns the maximum value of the utility function
def Decision(grid, max=True):
	depthLimit = 4
	start = time.clock()

	if max:
		return Maximize(grid=grid, alpha=-float('inf'), beta=float('inf'), depth=depthLimit, start=start)
	else:
		return Minimize(grid=grid,  alpha=-float('inf'), beta=float('inf'), depth=depthLimit, start=start)

#Finds the largest utility for the Max Player(Computer playing the game)
def Maximize(grid, alpha, beta, depth, start):
	if terminal(grid) or depth==0 or (time.clock()-start)>0.04:
		return Eval(grid)

	maxUtility =  -float('inf')

	#The children for the Max player are the neighboring tiles
	for child in children(grid):
		maxUtility = max(maxUtility, Minimize(grid=child, alpha=alpha, beta=beta, depth=depth-1, start=start))

		if maxUtility >= beta:
			break

		alpha = max(maxUtility, alpha)

	return maxUtility

#Finds the smallest utility for the Min Player
def Minimize(grid, alpha, beta, depth, start):
	if terminal(grid)  or depth==0 or (time.clock()-start)>0.04:
		return Eval(grid)

	minUtility = float('inf')
	children = []
	for pos in grid.getAvailableCells():
		current_grid2 = grid.clone()
		current_grid4 = grid.clone()

		current_grid2.insertTile(pos, 2)
		current_grid4.insertTile(pos, 4)

		children.append(current_grid2)
		children.append(current_grid4)

	#The children for the Min player
	for child in children:
		minUtility = min(minUtility, Maximize(grid=child,  alpha=alpha, beta=beta, depth=depth-1, start= start))
		if minUtility <= alpha:
			break
		beta = min(minUtility, beta)
	return minUtility

#==================================
#To impliment the Minmax algorithm
#==================================
#Returns the maximum value of the utility function
def Decision(grid, max=True):
	depthLimit = 4
	start = time.clock()

	if max:
		return Maximize(grid=grid, depth=depthLimit, start=start)
	else:
		return Minimize(grid=grid, depth=depthLimit, start=start)

#For the Max
def Maximize(grid, depth, start):
	if terminal(grid) or depth==0 or (time.clock()-start)>0.04:
		return Eval(grid)

	maxUtility =  -float('inf')

	#The children for the Max player
	for child in children(grid):
		maxUtility = max(maxUtility, Minimize(grid=child, depth=depth-1, start=start))

	return maxUtility

#For the Min
def Minimize(grid, depth, start):
	if terminal(grid)  or depth==0 or (time.clock()-start)>0.04:
		return Eval(grid)

	minUtility = float('inf')
	children = []
	for pos in grid.getAvailableCells():
		current_grid2 = grid.clone()
		current_grid4 = grid.clone()

		current_grid2.insertTile(pos, 2)
		current_grid4.insertTile(pos, 4)

		children.append(current_grid2)
		children.append(current_grid4)

	#The children for the Min player
	for child in children:
		minUtility = min(minUtility, Maximize(grid=child, depth=depth-1, start= start))

	return minUtility
