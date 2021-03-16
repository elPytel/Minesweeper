#By Pytel

import random
import copy

UNKNOWN = None
FREE = 0
MINE = -4

DEBUG = True

class Kombination:
	def __init__ (self, lenght, number):
		self.number_of_elements = number
		self.lenght = lenght
		self.position = self.Array(lenght)
		
	def Array (self, lenght):
		array = []
		for i in range(lenght):
			array.append(0)
		return array
		
	def Set (lenght, number):
		self.lenght = lenght
		self.number_of_elements = number
		self.position = self.Array(lenght)
		
	def Reset (self):
		self.position = 0
		self.position = self.Array(lenght)
		
	#def MakeBigger (self):
		#TODO
		
	def TransformToMines (self):
		kombination = []
		for number in self.array:
			if number == FREE:
				kombination.append(FREE)
			elif number == 1:
				kombination.append(MINE)
		return kombination
		
	def Next (self):
		self.MakeBigger()
		return TransformToMines()

class Player:
	def __init__ (self, y, x):
		self.board = []
		self.located_mines = []
		self.Y = y
		self.X = x
		self.next_to_clear = []
		
		self.located_mines = self.GenerateBoard()
		
	def GenerateBoard (self):
		board = []
		for y in range(self.Y):
			row = []
			for x in range(self.X):
				row.append(UNKNOWN)
			board.append(row)
		return board
	
	def CopyFree (self):
		for y in range(self.Y):
			for x in range(self.X):
				if self.located_mines[y][x] == UNKNOWN:
					if self.board[y][x] == FREE:
						self.located_mines[y][x] = FREE
		
	def RemoveUncovered (self):
		#for coord in self.next_to_clear:
		i = 0
		while i != len(self.next_to_clear):
			coord = self.next_to_clear[i]
			y = coord[0]
			x = coord[1]
			if self.board[y][x] != UNKNOWN:		# and self.board[y][x] >= FREE
				self.next_to_clear.remove(coord)
				print("Removed:", coord)
			else:
				i = i +1
	
	def IsBoard (self, y, x):
		if (y >= 0 and y < self.Y and x >= 0 and x < self.X):
			return True
		return False
		
	def FindUnknownAround(self, y, x):
		coord = []
		vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		for v in vector:
			yn = y +v[0]
			xn = x +v[1]
			if self.IsBoard(yn, xn) and self.board[yn][xn] == UNKNOWN:
				coord.append([yn, xn])
		return coord
		
	def FindMinesAround(self, y, x):
		coord = []
		vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		for v in vector:
			yn = y +v[0]
			xn = x +v[1]
			if self.IsBoard(yn, xn) and self.located_mines[yn][xn] == MINE:
				coord.append([yn, xn])
		return coord
	
	def FindMines (self):
		for y in range(self.Y):
			for x in range(self.X):
				# najde pozici s cislem 1-8
				if self.located_mines[y][x] != FREE and self.board[y][x] != UNKNOWN and self.board[y][x] > 0:
					unknown_arounds_coord = self.FindUnknownAround(y, x)
					unknown_arounds_number = len(unknown_arounds_coord)
					if DEBUG:
						print(unknown_arounds_coord)
						print(unknown_arounds_number)
					# pocet neznamych poli je stejny jako pocet min
					if unknown_arounds_number == self.board[y][x]:
						print("Nasel jsem vsechny sousedni miny.")
						self.board[y][x] = FREE
						self.located_mines[y][x] = FREE
						for coord in unknown_arounds_coord:
							yn = coord[0]
							xn = coord[1]
							self.located_mines[yn][xn] = MINE
			
	def FindNext (self):
		for y in range(self.Y):
			for x in range(self.X):
				# najde pozici s cislem 1-8
				if self.located_mines[y][x] != FREE and self.board[y][x] != UNKNOWN and self.board[y][x] > 0:
					mines_around_coords = self.FindMinesAround(y, x)
					mines_arounds_number = len(mines_around_coords)
					
					# pozici vsech okolnich min s urcitosti zname
					if mines_arounds_number == self.board[y][x]:
						coords = self.FindUnknownAround(y, x)
						
						# vybere souradnice bez min
						for mine in mines_around_coords:
							coords.remove(mine)
						
						# pridani bezpecnych souradnic do vyctu
						for coord in coords:
							if not coord in self.next_to_clear:
								self.next_to_clear.append(coord)
	
	def SolveByTry (self):
		#TODO
		# Rozdelit na podsektory
		# hleda neznamoou pozici
		"""
		for y in range(self.Y):
			for x in range(self.X):
		"""	
		# z ni cpousti floodfill, ktery obsahuje neznama pole, miny a konci na cislech
		# do vyhledavani pridava i cisla, ktera maji miny mimo jiz prohledanou oblast
		
		# nakopirovat podsektory i nalezenymi minami do vlstniho sendboxu, zaznamenat posunuti vyrezu
		sandbox = []
		
		# oznacit vsechny nezname pozice
		coords = []
		Y = 0
		X = 0
		for y in range(Y):
			for x in range(X):
				if sandbox[y][x] == UNKNOWN:
					coords.append([y,x])
					
		# vytvorit kombinace min pro tyto pozice (0-n min)
		# vyplnit okolni cisla
		# porovnat s originalem
		# pri uplne shode zaznamenat polohu min
		return None
		
	def RandomMove (self):
		valid = False
		
		# mini-max
		sandbox = self.GenerateBoard()
		for y in range(self.Y):
			for x in range(self.X):
				if self.located_mines[y][x] == UNKNOWN and self.board[y][x] == UNKNOWN:
					sandbox[y][x] = 0
		
		vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		# calculate probability
		for y in range(self.Y):
			for x in range(self.X):
				# najde pozici s cislem 1-8
				if self.located_mines[y][x] != FREE and self.board[y][x] != UNKNOWN and self.board[y][x] > 0:
					unknown_arounds_coord = self.FindUnknownAround(y, x)
					unknown_arounds_number = len(unknown_arounds_coord)
					
					for v in vector:
						yn = y +v[0]
						xn = x +v[1]
						if self.IsBoard(yn, xn) and self.board[yn][xn] == UNKNOWN:
							if sandbox[yn][xn] != UNKNOWN:
								sandbox[yn][xn] = sandbox[yn][xn] + self.board[y][x]/unknown_arounds_number
		print(sandbox)
		smallest = 10
		# find smallest
		for y in range(self.Y):
			for x in range(self.X):
				if sandbox[y][x] != UNKNOWN and sandbox[y][x] < smallest:
					smallest = sandbox[y][x]
		
		coords = []
		# locate all smallest
		for y in range(self.Y):
			for x in range(self.X):
				if sandbox[y][x] != UNKNOWN and sandbox[y][x] == smallest:
					coords.append([y,x])
		
		if len(coords) != 0:
			coord = random.choice(coords)		
		else:
			# random
			while not valid:
				y = random.randint(0,self.Y-1)
				x = random.randint(0,self.X-1)
				# check validity
				if self.board[y][x] == None and self.located_mines[y][x] != MINE:
					valid = True
			coord = [y, x]
		
		return coord
	
	def Move (self, board):
		self.board = board
		self.CopyFree()
		
		# odsrtrani jiz odhalena pole z self.next_to_clear
		self.RemoveUncovered()
		
		# musi hledat nove pozice
		if len(self.next_to_clear) == 0:
			self.FindMines()	# oznaci nove nalezene miny
			self.FindNext()		# najde nova volna pole
		
		# porad jsme nic nenasli
		if len(self.next_to_clear) == 0:
			self.SolveByTry()
			
		# porad jsme nic nenasli
		if len(self.next_to_clear) == 0:
			if DEBUG:
				print("Guessing the move.")
			move = self.RandomMove()
		else:
			if DEBUG:
				print("Clear:", self.next_to_clear)
			index = random.randint(0,len(self.next_to_clear)-1)
			move = self.next_to_clear.pop(index)
		
		if DEBUG:
			self.Print()
		return move
	
	def Print (self):
		print(" --- Player ---")
		for y in range(self.Y):
			for x in range(self.X):
				if self.board[y][x] == UNKNOWN:
					print("#", end='')
				elif self.board[y][x] == FREE:
					print("_", end='')
				elif self.board[y][x] == MINE:
					print("x", end='')
				else:
					print(self.board[y][x], end='')
				
			print("\t", end='')
			for x in range(self.X):
				if self.located_mines[y][x] == UNKNOWN:
					print("#", end='')
				elif self.located_mines[y][x] == FREE:
					print("_", end='')
				elif self.located_mines[y][x] == MINE:
					print("x", end='')
				else:
					print(self.located_mines[y][x], end='')
			print()
"""
END
"""