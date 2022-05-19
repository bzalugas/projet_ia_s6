import numpy as np
import math

# Global variables
grid = np.zeros((6,7), dtype=np.int8)
p1SymbolDefault = 'X'
p2SymbolDefault = 'O'
p1Symbol = ''
p2Symbol = ''


def initGrid():
	"""
	Initialise the grid
	"""
	return np.zeros((6,7), dtype=np.int8)

def chooseSymbols():
	"""
	Choose player symbols at start of the game
	"""
	global p1Symbol
	global p2Symbol
	p1Symbol = input("Choisissez le symbole du Joueur 1 (X par défaut) > ")
	p2Symbol = input("Choisissez le symbole du Joueur 2 (O par défaut) > ")
	p1Symbol = p1SymbolDefault if p1Symbol == '' else p1Symbol
	p2Symbol = p2SymbolDefault if p2Symbol == '' else p2Symbol

def getSymbol(gridValue):
	"""
	Get corresponding symbol for a value of the grid
	:param gridValue: the value of the player to convert
	"""
	if gridValue == 1:
		return str(p1Symbol)
	elif gridValue == 2:
		return str(p2Symbol)
	return ' '

def displayGrid(grid):
	"""
	Display the grid
	:param grid: the grid to display
	"""
	s = "\n\t_______________\n"
	for i in range(grid.shape[0]):
		s += "\t|"
		for j in range(grid.shape[1]):
			s += getSymbol(grid[i][j]) + "|"
		s += "\n"
	s += "\t---------------\n"
	s += "\t 1 2 3 4 5 6 7"
	print(s)

def getFreeRowOfCol(grid, col):
	"""
	Get the last free row of a column
	:param grid: the grid
	:param col: the column which find the free row
	"""
	lastFreeRow = -1
	if (col < 0 or col > 7):
		return lastFreeRow
	for i in range(grid.shape[0]):
		if (grid[i][col] == 0):
			lastFreeRow = i
	return int(lastFreeRow)

def checkDiagonal(grid, player):
	"""
	Check if a symbol is diagonally aligned
	:param grid: the grid where to find diagonal line-up
	:param player: the player for whom to look for the line-up
	"""
	for i in range(grid.shape[0] - 3):
		for j in range(grid.shape[1]):
			if (grid[i][j] == player and j <= grid.shape[1]-4):
				if (grid[i + 1][j + 1] == player and
				grid[i + 2][j + 2] == player and
				grid[i + 3][j + 3] == player):
					return True
			if (grid[i][j] == player and j >= grid.shape[1]-4):
				if (grid[i + 1][j - 1] == player and
				grid[i + 2][j - 2] == player and
				grid[i + 3][j - 3] == player):
					return True
	return False

def checkVertical(grid, player):
	"""
	Check if a symbol is vertically aligned
	:param grid: the grid where to find vertical line-up
	:param player: the player for whom to look for the line-up
	"""
	for i in range(grid.shape[0]-3):
		for j in range(grid.shape[1]):
			if (grid[i][j] == player):
				if (grid[i+1][j] == player and
				grid[i+2][j] == player and
				grid[i+3][j] == player):
					return True
	return False

def checkHorizontal(grid, player):
	"""
	Check if a symbol is horizontally aligned
	:param grid: the grid where to find horizontal line-up
	:param player: the player for whom to look for the line-up
	"""
	for i in range(grid.shape[0]):
		for j in range(grid.shape[1] - 3):
			if (grid[i][j] == player and j <= grid.shape[0]-4):
				if (grid[i][j+1] == player and
				grid[i][j+2] == player and
				grid[i][j+3] == player):
					return True
	return False

def checkFilledGrid(grid):
	"""
	Check if the grid is fulfilled
	:param grid: the grid
	"""
	for i in range(grid.shape[0]):
		for j in range (grid.shape[1]):
			if (grid[i][j] == 0):
				return False
	return True

def getWinner(grid):
	"""
	Get the winner of the game if finished
	:param grid: the grid in which to look for a winner
	"""
	if (checkDiagonal(grid, 1) or checkHorizontal(grid, 1) or checkVertical(grid, 1)):
		return 1
	if (checkDiagonal(grid, 2) or checkHorizontal(grid, 2) or checkVertical(grid, 2)):
		return 2
	return False

# coordinates = (row,col)
def placePiece(grid, player, coordinates):
	"""
	Place the piece of the player in the grid
	:param: grid the grid in which place the piece
	:param player: the player for whom place the piece
	:param coordinates: tuple reprensenting row and col
	"""
	grid[coordinates[0]][coordinates[1]] = player

################# IA PART #################

def player(state):
	"""
	Get which player should play in state
	:param state: the state
	"""
	nbPieces = 0
	for i in range(state.shape[0]):
		for j in range(state.shape[1]):
			if state[i][j] != 0:
				nbPieces += 1
	return 1 if nbPieces % 2 == 0 else 2

def getActions(state):
	"""
	Get possible actions in state
	:param state: state
	"""
	actions = []
	for j in range(state.shape[1]):
		i = getFreeRowOfCol(state, j)
		if (i != -1):
			actions.append((player(state), (i,j)))
	return actions

def result(state, action):
	"""
	Transition function. Defines the result of the action in the state
	:param state: the state in which do the action
	:param action: the action to do
	"""
	tmpState = state.copy()
	placePiece(tmpState, action[0], action[1])
	return tmpState

def terminalTest(state):
	"""
	The terminal test
	:param state: the state (=grid) to test
	"""
	if getWinner(state) != False or checkFilledGrid(state) == True:
		return True
	return False


def utility(state, player):
	"""
	Evaluation of the state
	:param state: the state (=grid) in which to calculate utility
	:param player: the num of the player (1 or 2)
	"""
	if getWinner(state) == player:
		return 1
	if getWinner(state) == False:
		return 0
	return -1

def successors(state):
	"""
	Get the result of each possible action
	:param state: state for which get results
	"""
	actions = getActions(state)
	succ = {}
	for a in actions:
		succ[a] = result(state, a)
	return succ

def minValue(state):
	"""
	Get the value for Min player
	:param state: state for which find value
	"""
	if (terminalTest(state)):
		return utility(state, 2)
	value = math.inf
	for a, s in successors(state).items():
		value = min(value, maxValue(state))
	return value

def maxValue(state):
	"""
	Get the value for Max player
	:param state: state for which find value
	"""
	if (terminalTest(state)):
		return utility(state, 1)
	value = -math.inf
	for a, s in successors(state).items():
		value = max(value, minValue(state))
	return value
	

def minimaxDecision(state):
	"""
	Move decision with minimax algorithm
	:param state: current state in game
	"""
	actions = getActions(state)
	dictActions = {}
	for a in actions:
		dictActions[a] = minValue(result(state, a))
	return max(dictActions, key=dictActions.get)

########################################################################

def askCol(player):
	"""
	Ask player for column to place piece
	:param player: the player who is asked
	"""
	return int(input("Joueur " + str(player) + " (" + getSymbol(player) + ") : colonne à remplir > "))

def fillGrid(grid, player):
	"""
	Place the next piece
	:param grid: the grid in which place the piece
	:param player: the player who is asked to place piece
	"""
	row = -1
	col = -1
	while (row == -1):
		col = askCol(player) - 1
		row = getFreeRowOfCol(grid, col)
	placePiece(grid, player, (row, col))

def askBeginPlayer(str):
	"""
	Ask who begins
	:param str: string to display for the input
	"""
	begin = -1
	while (begin != 'o' and begin != 'n'):
		begin = input(str)
	return 1 if begin == 'o' else 2

def displayEndGame(grid, winner):
	"""
	End game display
	:param grid: the final grid to display
	:param winner: the number of the player who won
	"""
	displayGrid(grid)
	again = ''
	str = ""
	if (winner != False):
		str = "Le joueur " + str(winner) + " a gagné !\nVoulez-vous rejouer ? (o/n) >"
	else:
		str = "Match nul.\nVoulez-vous rejouer ? (o/n) >"
	while (again != 'o' and again != 'n'):
		again = input(str).lower()
	return again

def playerVsComputerGameLoop(grid, level):
	"""
	The game loop for the game against computer
	:param grid: the starting grid
	"""
	chooseSymbols()

	beginPlayer = askBeginPlayer("Voulez-vous commencer (o/n) > ")
	currentPlayer = beginPlayer
	while (getWinner(grid) == False or checkFilledGrid(grid) == False):
		displayGrid(grid)
		if (currentPlayer == 1):
			#humain
			fillGrid(grid, currentPlayer)
			currentPlayer = 1 if currentPlayer == 2 else 2
		else:
			#ordi
			action = minimaxDecision(grid)
			placePiece(grid, 2, action[1])
	return grid, getWinner(grid)

def playerVsPlayerGameLoop(grid):
	"""
	The game loop
	:param grid: the starting grid
	"""
	chooseSymbols()

	currentPlayer = 1
	while (getWinner(grid) == False and checkFilledGrid(grid) == False):
		displayGrid(grid)
		fillGrid(grid, currentPlayer)
		currentPlayer = 1 if currentPlayer == 2 else 2
	return grid, getWinner(grid)

def askGame():
	"""
	Ask the user if he plays against human or machine
	"""
	choice = ''
	while (choice != 'h' and choice != 'o'):
		choice = input("Voulez-vous jouer contre un humain(h) ou contre l'ordinateur (o) ? > ")
	if (choice == 'o'):
		level = ''
		while (level != 'f' and level != 'm' and level != 'd'):
			level = input("Quel niveau de difficulté ?\nFacile = f\nMoyen = m\nDifficile = d\n > ")
		return level
	return 1

def game():
	"""
	The entire game
	"""
	playAgain = 'o'
	while (playAgain == 'o'):
		game = askGame()
		if game == 1:
			finalGrid, winner = playerVsPlayerGameLoop(initGrid())
		else:
			finalGrid, winner = playerVsComputerGameLoop(initGrid(), game)
		playAgain = displayEndGame(finalGrid, winner)
	print ('Au revoir !')

game()