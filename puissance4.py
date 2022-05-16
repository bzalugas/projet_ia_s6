import numpy as np

# Global variables
grid = np.zeros((6,7), dtype=np.int8)
p1SymbolDefault = 'X'
p2SymbolDefault = 'O'
p1Symbol = ''
p2Symbol = ''

"""
Initialise the grid 
"""
def initGrid():
	return np.zeros((6,7), dtype=np.int8)

"""
Choose player symbols at start of the game
"""
def chooseSymbols():
	global p1Symbol
	global p2Symbol
	p1Symbol = input("Choisissez le symbole du Joueur 1 (X par défaut) > ")
	p2Symbol = input("Choisissez le symbole du Joueur 2 (O par défaut) > ")
	p1Symbol = p1SymbolDefault if p1Symbol == '' else p1Symbol
	p2Symbol = p2SymbolDefault if p2Symbol == '' else p2Symbol

"""
Get corresponding value for a place on the grid
"""
def getSymbol(gridValue):
	if gridValue == 1:
		return str(p1Symbol)
	elif gridValue == 2:
		return str(p2Symbol)
	return ' '
"""
Display the grid
"""
def displayGrid(grid):
	s = "\n\t_______________\n"
	for i in range(grid.shape[0]):
		s += "\t|"
		for j in range(grid.shape[1]):
			s += getSymbol(grid[i][j]) + "|"
		s += "\n"
	s += "\t---------------\n"
	s += "\t 1 2 3 4 5 6 7"
	print(s)

"""
Get the last free row of a column
"""
def getFreeRowOfCol(grid, col):
	lastFreeRow = -1
	if (col < 0 or col > 7):
		return lastFreeRow
	for i in range(grid.shape[0]):
		if (grid[i][col] == 0):
			lastFreeRow = i
	return lastFreeRow

"""
Check if a symbol is diagonally aligned
"""
def checkDiagonal(grid, player):
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

"""
Check if a symbol is vertically aligned
"""
def checkVertical(grid, player):
	for i in range(grid.shape[0]-3):
		for j in range(grid.shape[1]):
			if (grid[i][j] == player):
				if (grid[i+1][j] == player and
				grid[i+2][j] == player and
				grid[i+3][j] == player):
					return True
	return False

"""
Check if a symbol is horizontally aligned
"""
def checkHorizontal(grid, player):
	for i in range(grid.shape[0]):
		for j in range(grid.shape[1] - 3):
			if (grid[i][j] == player and j <= grid.shape[0]-4):
				if (grid[i][j+1] == player and
				grid[i][j+2] == player and
				grid[i][j+3] == player):
					return True
	return False

"""
Get the winner of the game if it's finished
"""
def getWinner(grid):
	if (checkDiagonal(grid, 1) or checkHorizontal(grid, 1) or checkVertical(grid, 1)):
		return 1
	if (checkDiagonal(grid, 2) or checkHorizontal(grid, 2) or checkVertical(grid, 2)):
		return 2
	return False

"""
Ask player for column to place piece
"""
def askCol(player):
	return int(input("Joueur " + str(player) + " (" + getSymbol(player) + ") : colonne à remplir > "))

"""
Set column to player symbol
"""
def fillGrid(grid, player):
	row = -1
	while (row == -1):
		col = askCol(player) - 1
		row = getFreeRowOfCol(grid, int(col))
	grid[row][col] = player
	print (str(grid[row][col]))

"""
Ask who begins
"""
def askBeginPlayer():
	begin = -1
	while (begin != 1 and begin != 2):
		begin = int(input("Qui commence ? (1/2) > "))
	return begin

"""
End game display
"""
def endGame(grid, winner):
	displayGrid(grid)
	again = ''
	while (again != 'o' and again != 'n'):
		again = input("Le joueur " + str(winner) + " a gagné !\nVoulez-vous rejouer ? (o/n) >").lower()
	return again

"""
The game loop
"""
def gameLoop(grid):
	chooseSymbols()

	beginPlayer = askBeginPlayer()
	currentPlayer = beginPlayer
	while (getWinner(grid) == False):
		displayGrid(grid)
		fillGrid(grid, currentPlayer)
		currentPlayer = 1 if currentPlayer == 2 else 2
	return grid, getWinner(grid)

"""
The entire game
"""
def game():
	playAgain = 'o'
	while (playAgain == 'o'):
		finalGrid, winner = gameLoop(initGrid())
		playAgain = endGame(finalGrid, winner)
	print ('Au revoir !')

game()