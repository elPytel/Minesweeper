#By Pytel

import random
import copy

#class Board:
	
"""
1-8	pocet min
0	prazdne pole, odhalene
-1	chyba
None	skryte
-4	mina
"""
FREE = 0
MINE = -4
UNKNOWN = None

DEBUG = True

class Game:
	
	def __init__ (self, number=0, y=0, x=0):
		self.pattern = []
		self.board = []
		self.mines = number		# pocet min
		self.hiden = x*y
		self.board_size_x = x
		self.board_size_y = y
		self.end = False
		self.exploded = False
		
	def GenerateBoard (self):
		board = []
		for y in range(self.board_size_y):
			row = []
			for x in range(self.board_size_x):
				row.append(UNKNOWN)
			board.append(row)
		return board
	
	def PlaceMines (self):
		placed = 0
		while placed < self.mines:
			y = random.randint(0, self.board_size_y-1)
			x = random.randint(0, self.board_size_x-1)
			if self.pattern[y][x] == UNKNOWN:
				self.pattern[y][x] = MINE		# je tam mina
				placed = placed +1
			
	def IsBoard (self, y, x):
		if (y >= 0 and y < self.board_size_y and x >= 0 and x < self.board_size_x):
			#print("Valid coord")
			return True
		return False
		
	def CountMines (self, y, x):
		mines = 0
		vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		for v in vector:
			yn = y +v[0]
			xn = x +v[1]
			#print("y:", yn, "	x:", xn)
			if self.IsBoard(yn, xn) and self.pattern[yn][xn] == MINE:
				#print("mine found!")
				mines = mines +1
		#print(mines)
		return mines
		
	def CalculateNumbers (self):
		for y in range(self.board_size_y):
			for x in range(self.board_size_x):
				if self.pattern[y][x] == UNKNOWN:
					self.pattern[y][x] = self.CountMines(y, x)
		
	def NewGame (self):
		self.pattern = self.GenerateBoard()
		self.board = self.GenerateBoard()
		self.PlaceMines()
		self.CalculateNumbers()
		self.hiden = self.board_size_x*self.board_size_y
		self.end = False
		self.exploded = False
		
		if self.hiden == 0:
			self.end = True
			return False
		
	def IsEnd (self):
		return self.end
	
	def IsExploded (self):
		return self.exploded
		
	def GetBoard (self):
		return copy.deepcopy(self.board)
	
	def IsValidMove (self, move):
		if move == None or len(move) != 2:
			return False
		y = move[0]
		x = move[1]
		if self.IsBoard(y, x) == False:
			return False
		if self.board[y][x] == UNKNOWN:
			return True
		return False
			
	def FloodFill (self, y, x):
		self.board[y][x] = self.pattern[y][x]	# resolve seed
		
		searched = []
		unsearched = [[y,x]]
		while len(unsearched) != 0:
			coord = unsearched.pop(0)
			#vector = [[0,1],[1,0],[0,-1],[-1,0]]
			vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
			for v in vector:
				yn = coord[0] +v[0]
				xn = coord[1] +v[1] 
				if 0 and DEBUG:
					print("Next place - y:", yn, "	x:", xn)
				if self.IsBoard(yn, xn) and not [yn,xn] in searched:
				#if self.IsBoard(yn, xn) and IsNotIn(coord, searched):
					if 0 and  DEBUG:
						print("valid")
					place = self.pattern[yn][xn]
					if place == 0 and not [yn,xn] in unsearched:
					#if place == 0 and IsNotIn(coord, unsearched):
						unsearched.append([yn, xn])
					self.board[yn][xn] = place
				
			# zaradi mezi prohledane
			searched.append(coord)
			if 0 and DEBUG:
				print("searched:", searched)
				print("unsearched:",unsearched)
			
		
	def Uncovered (self):
		uncovered = 0
		for y in range(self.board_size_y):
			for x in range(self.board_size_x):
				if self.board[y][x] == UNKNOWN:
					uncovered = uncovered +1
		return uncovered
		
	def Execute (self, move):
		y = move[0]
		x = move[1]
		if self.board[y][x] != UNKNOWN:
			return False
		
		if self.pattern[y][x] == MINE:		# slapl na minu
			self.board[y][x] = MINE
			self.end = True
			self.exploded = True
			if DEBUG:
				print("Mine!")
		elif self.pattern[y][x] == FREE:	# nasel volne pole
			self.FloodFill(y, x)
			if DEBUG:
				print("Free!")
		else:								# nasel pole obklopene minami
			self.board[y][x] = self.pattern[y][x]
			if DEBUG:
				print("Soo close!")
		
		self.hiden = self.Uncovered()
		if self.hiden == self.mines:
			self.end = True
	
	def PrintMines (self):
		print(" --- Mines ---")
		#print(self.pattern)
		for y in range(self.board_size_y):
			for x in range(self.board_size_x):
				if self.pattern[y][x] == FREE:
					print("_", end='')
				elif self.pattern[y][x] == MINE:
					print("x", end='')
				else:
					print(self.pattern[y][x], end='')
			print()
		
	def Print (self):
		print(" --- Game board ---")
		#print(self.board)
		for y in range(self.board_size_y):
			for x in range(self.board_size_x):
				if self.board[y][x] == UNKNOWN:
					print("#", end='')
				elif self.board[y][x] == FREE:
					print("_", end='')
				elif self.board[y][x] == MINE:
					print("x", end='')
				else:
					print(self.board[y][x], end='')
			print()
		
def IsNotIn (what, where):
	for item in where:
		if item == what:
			return False
	return True

"""
END
"""