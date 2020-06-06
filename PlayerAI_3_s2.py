#AIM: PLAYER_AI GETS THE NEXT MOVE FOR THE PLAYER 


from BaseAI_3 import BaseAI
from Helper import *
from Minimaxab import *
from Grid_3 import *
import numpy as np

class PlayerAI(BaseAI):
	def getMove(self, grid):
		moves = grid.getAvailableMoves()
		maxUtility = -np.inf
		nextDir = -1

		for move in moves:
			child = getChild(grid, move)

			utility = Decision(grid=child, max=False) 

			if utility >= maxUtility:
				maxUtility = utility
				nextDir = move

		return nextDir


#AIM: IMPLEMENTS SEVERAL HELPER FUNCTIONS USED FOR GETTING THE NEXT MOVE
import math
import time

#For log file
import logging


logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',filename = "run2048_"+str(time.clock())+".log")
logger = logging.getLogger(__name__)


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


#Evaluates the heuristic. The heuristic used here is a gradient function
def Eval_3(grid):
	import math
	#import numpy as np

	if terminal(grid):
		return -float('inf')

	#gradients = [
	#			[[ 3,  2,  1,  0],[ 2,  2,  0, -1],[ 1,  0, -1, -2],[ 0, -1, -2, -3]],
	#			[[ 0,  1,  2,  3],[-1,  0,  2,  2],[-2, -1,  0,  1],[-3, -2, -1, -0]],
	#			[[ 0, -1, -2, -3],[ 1,  0, -1, -2],[ 2,  2,  0, -1],[ 3,  2,  1,  0]],
	#			[[-3, -2, -1,  0],[-2, -1,  0,  1],[-1,  0,  2,  2],[ 0,  1,  2,  3]]
	#			]
	gradients = [
				[[ 1,  0.868,  0.754,  0.654],[ 0.868,  0.754,  0.654, 0.531],[ 0.754,  0.654, 0.531, 0.493],[ 0.654, 0.531, 0.493, 0.449]],
				[[ 0.654,  0.754,  0.806,  1],[0.531,  0.654,  0.754,  0.868],[0.493, 0.531,  0.654,  0.754],[0.449, 0.493, 0.531, 0.654]],
				[[ 0.65, 0.53, 0.493, 0.449],[ 0.75,  0.65, 0.53, 0.49],[ 0.868,  0.754,  0.654, 0.531],[ 1, 0.868,  0.754, 0.654 ]],
				[[0.449, 0.493, 0.531,  0.654],[0.493, 0.531,  0.654,  0.754],[0.531,  0.654,  0.754,  0.868],[ 0.654,  0.754,  0.868,  1]]
				]

	values = [0,0,0,0]

	for i in range(4):
		for x in range(4):
			for y in range(4):
				values[i] += gradients[i][x][y]*grid.map[x][y]


	return max(values)

# To get the Max Value of a grid
def Eval_1(grid):
    if terminal(grid):
        return -float('inf')

    maxValue = grid.getMaxTile()
    score = maxValue
    return score

# To claculate the utility related to the number of available cells
def Eval_2(grid):
    import math

    if terminal(grid):
        return -float('inf')

    score = numOfAvailableCells(grid)
    #score = filter(score)
    return score

# TO calculation the number of available cells
def numOfAvailableCells(grid):
    num = len(grid.getAvailableCells())
    return num

# To filter the numOfAvailableCells()
def filter(num):
    if num > 7:
        num = 0
        return num
    else:
        return num

def Eval(grid):
    #E1 = 2.5*Eval_1(grid)
    #E2 = 63*Eval_2(grid)
    E3 = Eval_1(grid)
    #logger.info("E1= {}   E2= {}  E3= {}".format(E1,E2,E3))
    #score = E1 + E2 + E3
    score = E3
    logger.info("MaxTile= {}".format(grid.getMaxTile()))
    return score
    #return 0.0008*Eval_1(grid) + 0.02*Eval_2(grid)+ 0.0003*Eval_3(grid) # 1024
#AIM: IMPLEMENTS THE MINIMAX ALGORITHM WITH ALPHA-BETA PRUNING

from Helper import *
import numpy as np
import time 


#Returns the maximum value of the utility function
def Decision(grid, max=True):
	limit = 4
	start = time.clock()

	if max:
		return Maximize(grid=grid, alpha=-np.inf, beta=np.inf, depth=limit, start=start)
	else:
		return Minimize(grid=grid,  alpha=-np.inf, beta=np.inf, depth=limit, start=start)
		

#Finds the largest utility for the Max Player(Computer playing the game)
def Maximize(grid, alpha, beta, depth, start):
	if terminal(grid) or depth==0 or (time.clock()-start)>0.04:
		return Eval(grid)

	maxUtility =  -np.inf
	
	#The children for the Max player are the neighboring tiles 
	for child in children(grid):
		maxUtility = max(maxUtility, Minimize(grid=child, alpha=alpha, beta=beta, depth=depth-1, start=start))

		if maxUtility >= beta:
			break

		alpha = max(maxUtility, alpha)

	return maxUtility


#Finds the smallest utility for the Min Player(Computer placing the random tiles)
def Minimize(grid, alpha, beta, depth, start):
	if terminal(grid)  or depth==0 or (time.clock()-start)>0.04:
		return Eval(grid)

	minUtility = np.inf 

	empty = grid.getAvailableCells();

	children = []

	for pos in empty:
		current_grid2 = grid.clone()
		current_grid4 = grid.clone()

		current_grid2.insertTile(pos, 2)
		current_grid4.insertTile(pos, 4)

		children.append(current_grid2)
		children.append(current_grid4)

	#The children for the Min player include all random tile possibilities for the current state 
	for child in children:
		minUtility = min(minUtility, Maximize(grid=child,  alpha=alpha, beta=beta, depth=depth-1, start= start))
		
		if minUtility <= alpha:
			break

		beta = min(minUtility, beta)

	return minUtility
