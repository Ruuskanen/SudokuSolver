import sys
import random
import console

class Square:
	def __init__(self, value, permanent, xcoord, ycoord, subgrid, square):
		self.value = value
		self.permanent = permanent
		self.xcoord = xcoord
		self.ycoord = ycoord
		self.subgrid = subgrid
		self.square = square
		self.possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		
def initializeGrid():
	i = 1
	grid = []
	for y in range(1, 10):
		for x in range(1, 10):
			square = Square(0, False, x, y, 0, i)
			grid.append(square)
			i += 1
	addStartValues(grid)
	addSubgrids(grid)
	addPermanent(grid)
	return grid
	
def printGrid():
	for i, square in enumerate(grid):
		if (i % 3 == 0 and square.xcoord != 1):
			sys.stdout.write("|".ljust(3))
		if square.value == 0:
			sys.stdout.write("_".ljust(3))
		else:
			sys.stdout.write("".join(str(grid[i].value)).ljust(3))
		if square.xcoord == 9:
			print()
			if square.ycoord == 3 or square.ycoord == 6:
				print("-" * 31)
			elif square.ycoord != 9:
				print(" " * 9 + "|" + " " * 11 + "|")
	print()
				
def printPossibleNumbersForSquares():
	for i, square in enumerate(grid):
		if len(square.possibleNumbers) != 0:
			print("Square " + str(square.square) + ": " + str(square.possibleNumbers))
		else:
			if square.value != 0:
				print("Square " + str(square.square) + ": Oikea arvo ratkaistu.")
			else:
				print("Square " + str(square.square) + ": Ei löydettävissä oikeaa ratkaisua.") 

def printSquaresWithOnePossibleNumber():
	for i in range(0, 81):
		if len(grid[i].possibleNumbers) == 1:
			print("Square " + str(i + 1) + ": " + str(grid[i].possibleNumbers))
											
def printFirstSquareWithOnePossibleNumber():
	for i in range(0, 81):
		if len(grid[i].possibleNumbers) == 1:
			print("Square " + str(i + 1) + ": " + str(grid[i].possibleNumbers))
			break
																						
def checkRow(index, value):
	for j in range(0, 81):
		if grid[j].ycoord == grid[index].ycoord:
			if grid[j].value == value:
				return False
	return True

def checkColumn(index, value):
	for j in range(0, 81):
		if grid[j].xcoord == grid[index].xcoord:
			if grid[j].value == value:
				return False
	return True
	
def checkSubgrid(index, value):
	for j in range(0, 81):
		if grid[j].subgrid == grid[index].subgrid:
			if grid[j].value == value:
				return False
	return True
	
def checkAll(index, value):
	if checkRow(index, value) == False:
		return False
	if checkColumn(index, value) == False:
		return False
	if checkSubgrid(index, value) == False:
		return False
	return True
	
def checkSudoku():
	for i in range(0, 81):
		if grid[i].value != 0:
			currentValue = grid[i].value
			grid[i].value = 0
			check = checkAll(i, currentValue)
			grid[i].value = currentValue
			if check == False:
				return False
	return True
	
def checkIfSudokuIsComplete():
	for square in grid:
		if square.value == 0:
			return False	
	return True
	
def addRow(row, list, grid):
	for i in range(0, 9):
		for square in grid:
			if row == square.ycoord and i + 1 == square.xcoord:
				square.value = list[i]
				
def addPermanent(grid):
	for square in grid:
		if square.value != 0:
			square.permanent = True
	
def addSubgrids(grid):
	for i in range(0, 81):
		if grid[i].ycoord < 4:
			if grid[i].xcoord < 4:
				grid[i].subgrid = 1
			elif grid[i].xcoord < 7:
				grid[i].subgrid = 2
			else:
				grid[i].subgrid = 3
		elif grid[i].ycoord < 7:
			if grid[i].xcoord < 4:
				grid[i].subgrid = 4
			elif grid[i].xcoord < 7:
				grid[i].subgrid = 5
			else:
				grid[i].subgrid = 6
		elif grid[i].ycoord < 10:
			if grid[i].xcoord < 4:
				grid[i].subgrid = 7
			elif grid[i].xcoord < 7:
				grid[i].subgrid = 8
			else:
				grid[i].subgrid = 9
	
def updatePossibleNumbersByValues(): # Funktio käy ruudut läpi vuorotellen, ja päivittää mahdolliset numerot muiden samalla rivillä/sarakkeella/neliöllä olevien ruutujen arvojen perusteella.
	for i in range(0, 81):
		if grid[i].value != 0:
			grid[i].possibleNumbers = []
		else:
			for j in range(0, 81):
				if grid[j].value != 0:
					if grid[j].xcoord == grid[i].xcoord:
						if grid[j].value in grid[i].possibleNumbers:
							grid[i].possibleNumbers.remove(grid[j].value)
					if grid[j].ycoord == grid[i].ycoord:
						if grid[j].value in grid[i].possibleNumbers:
							grid[i].possibleNumbers.remove(grid[j].value)
					if grid[j].subgrid == grid[i].subgrid:
						if grid[j].value in grid[i].possibleNumbers:
							grid[i].possibleNumbers.remove(grid[j].value)
	
def updatePossibleNumbersByRowColumnSubgrid(): # Funktio käy ruudut läpi vuorotellen, ja päättelee sopiiko ruutuun vain yksi arvo riviltä/sarakkeelta/neliöltä puuttuvien lukujen perusteella.
	for i, isquare in enumerate(grid):
		#for n in range(0, len(isquare.possibleNumbers)):
		for number in isquare.possibleNumbers:
			yCheck = True
			xCheck = True
			subgridCheck = True
			for j, jsquare in enumerate(grid):
				if i != j:
					if isquare.ycoord == jsquare.ycoord:
						#print(isquare.possibleNumbers[n])
						if number in jsquare.possibleNumbers:
							yCheck = False
					if isquare.xcoord == jsquare.xcoord:
						if number in jsquare.possibleNumbers:
							xCheck = False
					if isquare.subgrid == jsquare.subgrid:
						if number in jsquare.possibleNumbers:
							subgridCheck = False
			if yCheck == True:
				isquare.possibleNumbers = [number]
			elif xCheck == True:
				isquare.possibleNumbers = [number]
			elif subgridCheck == True:
				isquare.possibleNumbers = [number]	

def updatePossibleNumbersForSquares(): # Funktio päivittää mahdolliset arvot ruutuihin. Älä tee funktioita, jotka lisäävät arvoja mahdollisten arvojen joukkoon. Funktioiden kutsumisjärjestyksellä on väliä.
	updatePossibleNumbersByValues()
	updatePossibleNumbersByRowColumnSubgrid()
							
def checkForObviousValues():
	for i in range(0, 81):
		if len(grid[i].possibleNumbers) == 1:
			return True
	return False
	
def checkForSquareWithNoSolution():
	for square in grid:
		if square.value == 0 and square.possibleNumbers == []:
			return True
	return False

def fillRandomObviousValue(): # Funktio täyttää ruudukkoon satunnaisen itsestäänselvän arvon. 
	global count
	list = []
	for i in range(0, 81):
		if len(grid[i].possibleNumbers) == 1:
			list.append(i)
	index = random.choice(list)
	print("Rivi " + str(grid[index].ycoord) + ", Sarake " + str(grid[index].xcoord) + ": " + str(grid[index].possibleNumbers))
	cmd = input()
	if cmd == "":
		grid[index].value = grid[index].possibleNumbers[0]
		grid[index].permanent = True
		count += 1
		console.clear()
									
def increment1(index):
	i = 1
	while True:
		if checkAll(index, grid[index].value + i) == True:
			grid[index].value += i
			return grid[index].value
			break
		else:
			i += 1
			
def solveSudoku():
	global count
	i = 0
	while 0 <= i < 81:
		if grid[i].permanent == True:
			i += 1
		else:
			newValue = increment1(i)
			if newValue != 10:
				i += 1
			elif newValue == 10:
				grid[i].value = 0
				while True:
					i -= 1
					if grid[i].permanent == False:
						break
		
def bruteForceSudoku():		
	while True:
		print("Start position:")
		print()
		printGrid()
		if checkSudoku() == False:
			print("Start Position is not allowed.")
			break
		print("Solving sudoku...")
		print()
		solveSudoku()
		if checkSudoku() == False:
			print("Solved sudoku contains errors...") # This should never happen..
		print()
		printGrid()
		break
		
# Start Values

def addStartValues(grid):
	row1 = [0,0,0,  0,0,0,  0,0,0]
	addRow(1, row1, grid)
	row2 = [0,0,0,  0,0,0,  0,0,0]
	addRow(2, row2, grid)
	row3 = [0,0,0,  0,0,0,  0,0,0]
	addRow(3, row3, grid)
	
	row4 = [0,0,0,  0,0,0,  0,0,0]
	addRow(4, row4, grid)
	row5 = [0,0,0,  0,0,0,  0,0,0]
	addRow(5, row5, grid)
	row6 = [0,0,0,  0,0,0,  0,0,0]
	addRow(6, row6, grid)
	
	row7 = [0,0,0,  0,0,0,  0,0,0]
	addRow(7, row7, grid)
	row8 = [0,0,0,  0,0,0,  0,0,0]
	addRow(8, row8, grid)
	row9 = [0,0,0,  0,0,0,  0,0,0]
	addRow(9, row9, grid)
		
# Solving Sudoku

grid = initializeGrid()
updatePossibleNumbersForSquares()
bruteForceSudoku()


