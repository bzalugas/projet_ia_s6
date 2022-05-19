import numpy as np

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
	return lastFreeRow

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

################# IA PART #################

def terminalTest(state):
	"""
	The terminal test
	:param state: the state (=grid) to test
	"""
	return True if getWinner(state) != False else False

def utility(state, player):
	"""
	Evaluation of the state
	:param state: the state (=grid) in which to calculate utility
	:param player: the num of the MAX player (1 or 2)
	"""
	if getWinner(state) == player:
		return 1
	if getWinner(state) == False:
		return 0
	return -1

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
	while (row == -1):
		col = askCol(player) - 1
		row = getFreeRowOfCol(grid, int(col))
	grid[row][col] = player
	print (str(grid[row][col]))

def askBeginPlayer():
	"""
	Ask who begins
	"""
	begin = -1
	while (begin != 1 and begin != 2):
		begin = int(input("Qui commence ? (1/2) > "))
	return begin

def endGame(grid, winner):
	"""
	End game display
	:param grid: the final grid to display
	:param winner: the number of the player who won
	"""
	displayGrid(grid)
	again = ''
	while (again != 'o' and again != 'n'):
		again = input("Le joueur " + str(winner) + " a gagné !\nVoulez-vous rejouer ? (o/n) >").lower()
	return again

def playerVsPlayerGameLoop(grid):
	"""
	The game loop
	:param grid: the starting grid
	"""
	chooseSymbols()

	beginPlayer = askBeginPlayer()
	currentPlayer = beginPlayer
	while (getWinner(grid) == False):
		displayGrid(grid)
		fillGrid(grid, currentPlayer)
		currentPlayer = 1 if currentPlayer == 2 else 2
	return grid, getWinner(grid)

def game():
	"""
	The entire game
	"""
	playAgain = 'o'
	while (playAgain == 'o'):
		finalGrid, winner = playerVsPlayerGameLoop(initGrid())
		playAgain = endGame(finalGrid, winner)
	print ('Au revoir !')

game()