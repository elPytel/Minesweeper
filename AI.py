#By Pytel

import random
import copy

UNKNOWN = None
FREE = 0
MINE = -4

DEBUG = True
# nastaveni kombinaci
MIN_FREE = 10
MAX_UNKNOWN = 18

class Kombination:
	def __init__ (self, lenght=0, number=0):
		self.number_of_elements = number
		self.lenght = lenght
		self.Reset()
	
	# vytvori pole zadane delky	
	def Array (self, lenght):
		array = []
		for i in range(lenght):
			array.append(0)
		return array
		
	def Reset (self):
		self.position = -1
		self.array = self.Array(self.lenght)
		
	def Set (self, lenght, number):
		self.lenght = lenght
		self.number_of_elements = number
		self.Reset()
	
	# ukoncivaci test	
	def IsLast (self, binary):
		ret = False
		# kombinaci same miny prohlasi za posledni a ukonci se
		if binary == self.lenght*'1':
			ret = True
		return ret
		
	def PositionToKombination (self):
		ret = True
		if self.number_of_elements == 2:
			binary = bin(self.position).replace("0b", "")
			for i in range(len(binary)):
				index = self.lenght +i -len(binary)
				self.array[index] = int(binary[i])
			if self.IsLast(binary):
				ret = False
		else:
			print("ERROR, not implemented")
			ret = False
		
		return ret
	
	# vrazi true, pokud existuje dalsi prvek	
	def MakeBigger (self):
		self.position = self.position +1
		return self.PositionToKombination()
		
	# specificka funkce AI_MINY
	def TransformToMines (self):
		kombination = []
		for number in self.array:
			if number == 0:
				kombination.append(FREE)
			elif number == 1:
				kombination.append(MINE)
		return kombination
	
	# zvenci volana funkce	
	def Next (self):
		if self.MakeBigger() == False:
			return None
		return self.TransformToMines()

class Player:
	def __init__ (self, y, x):
		self.board = []
		self.located_mines = []
		self.Y = y
		self.X = x
		self.next_to_clear = []
		self.min_free = MIN_FREE	# od jakeho poctu jiz ma smysl spustit flood fill
		self.max_unknown = MAX_UNKNOWN
		self.located_mines = self.GenerateBoard()
		
	def GenerateBoard (self):
		board = []
		for y in range(self.Y):
			row = []
			for x in range(self.X):
				row.append(UNKNOWN)
			board.append(row)
		return board
	
	# nakopuje prazdne pozice do vlastni datove struktury
	def CopyFree (self):
		for y in range(self.Y):
			for x in range(self.X):
				if self.located_mines[y][x] == UNKNOWN:
					if self.board[y][x] == FREE:
						self.located_mines[y][x] = FREE
		
	# kotroluje zda nechce hrat na jiz odkryte prazdne pozice
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
	
	# jsou to validni souradnice?
	def IsBoard (self, Y, X, y, x):
		if (y >= 0 and y < Y and x >= 0 and x < X):
			return True
		return False
	
	# vrati souradnice prazdnych okolnich poli v self.board
	def FindUnknownAround(self, y, x):
		coords = []
		vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		for v in vector:
			yn = y +v[0]
			xn = x +v[1]
			if self.IsBoard(self.Y, self.X, yn, xn) and self.board[yn][xn] == UNKNOWN:
				coords.append([yn, xn])
		return coords
		
	# najde pozice s prilehlimy minami
	def FindMinesAround(self, y, x):
		coord = []
		vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		for v in vector:
			yn = y +v[0]
			xn = x +v[1]
			if self.IsBoard(self.Y, self.X, yn, xn) and self.located_mines[yn][xn] == MINE:
				coord.append([yn, xn])
		return coord
		
	# najde pozice s prilehlimy cisli
	def FindNumbersAround(self, y, x):
		coord = []
		vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		for v in vector:
			yn = y +v[0]
			xn = x +v[1]
			if self.IsBoard(self.Y, self.X, yn, xn) and self.board[yn][xn] != UNKNOWN:
				if self.board[yn][xn] >= FREE:
					coord.append([yn, xn])
		return coord
		
	# oznaci kde jsou miny
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
						print(self.board[y][x])
						self.board[y][x] = FREE
						self.located_mines[y][x] = FREE
						for coord in unknown_arounds_coord:
							yn = coord[0]
							xn = coord[1]
							self.located_mines[yn][xn] = MINE
	
	# najde prazdne pozice k dalsimu tahu
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
	
	# najde pozice daneho typu a vrati jejich souradnice
	def Find (board, attribute):
		Y = len(board)
		X = len(board[0])
		coord = []
		for y in range(Y):
			for x in range(X):
				if board[y][x] == attribute:
					coord.append([y, x, attribute])
		return coord
		
	# najde nezname pozice v self.board
	def FindUnknown (self):
		coord = []
		for y in range(self.Y):
			for x in range(self.X):
				if self.board[y][x] == UNKNOWN and self.located_mines[y][x] != MINE:
					coord.append([y, x])
		return coord
				
	# najde okrajove souradnice pro oriznuti vybraneho vyctu souradnic
	def FindCropp (self, coords):
		min_y = self.Y 
		max_y = 0 
		min_x = self.X
		max_x = 0
		for coord in coords:
			y = coord[0]
			x = coord[1]
			if min_y > y:
				min_y = y
			elif max_y < y:
				max_y = y
				
			if min_x > x:
				min_x = x
			elif max_x < x:
				max_x = x
			
		cropp = [min_y, max_y, min_x, max_x]
		return cropp
		
	# vytvori pole zadanych rozmeru a vyplni FREE
	def MakeFreeBoard (self, Y, X):
		board = []
		for y in range(Y):
			row = []
			for x in range(X):
				row.append(FREE)
			board.append(row)
		return board
		
	# porovna zda obsahuje na kritickych pozicichstejna cisla, jsou tedy ekvivalentni
	def BoardsAreMatch (self, template, board, Y, X):
		ret = True
		for y in range(Y):
			for x in range(X):
				if template[y][x] != None and template[y][x] > FREE:
					if template[y][x] != board[y][x]: 
						ret = False
						return ret
		return ret
		
	# spocita miny prilehle k danemu poly
	def CountMines (self, board, y, x):
		Y = len(board)
		X = len(board[0])
		mines = 0
		vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
		for v in vector:
			yn = y +v[0]
			xn = x +v[1]
			if self.IsBoard(Y, X, yn, xn) and board[yn][xn] == MINE:
				#print("mine found!")
				mines = mines +1
		#print(mines)
		return mines
		
	# vypocte cisla min v poly
	def CalculateNumbers (self, board):
		Y = len(board)
		X = len(board[0])
		for y in range(Y):
			for x in range(X):
				if board[y][x] == FREE:
					board[y][x] = self.CountMines(board, y, x)
	
	# rozhodne zda ji ma flood fill prohledavat
	def IsQualifiedToAppend (self, start, to):
		ret = False
		# from
		y = start[0]
		x = start[1]
		# to
		yn = to[0]
		xn = to[1]
		
		from_place = self.board[y][x]
		to_place = self.board[yn][xn]
		if from_place == UNKNOWN:		# pokud jde z neznemo pozice
			if to_place != FREE:
				ret = True
		elif from_place > FREE: 		# pokud jde z cisla
			if to_place == UNKNOWN:
				ret = True
		else:
			ret = False
		return ret
	
	# testovani zda obsahuje dane souradnice
	def IsIn (what, where):
		for item in where:
			if item[0] == what[0] and item[1] == what[1]:
				return True
		return False
	
	# vrati souradnice vsechspojenych pozic s jejich obsahem
	# cisla, nezname pozice, i miny
	def FloodFill (self, coord):
		y = coord[0]
		x = coord[1]
		if DEBUG:
			print("Spoustim flood fill, seed:", y, x)
				
		searched = []
		unsearched = [[y,x, None]]
		while len(unsearched) != 0:
			coord = unsearched.pop(0)
			vector = [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]
			for v in vector:
				yn = coord[0] +v[0]
				xn = coord[1] +v[1] 
				if 0 and DEBUG:
					print("Next place - y:", yn, "	x:", xn)
				
				in_board = self.IsBoard(self.Y, self.X, yn, xn)
				not_searched = not Player.IsIn([yn,xn], searched)
				if in_board and not_searched:
					if 0 and DEBUG:
						print("valid")
					
					not_unsearched = not Player.IsIn([yn,xn], unsearched)
					valid_to_add = self.IsQualifiedToAppend([y,x], [yn,xn])
					if not_unsearched and valid_to_add:
						place = self.board[yn][xn]
						if place == UNKNOWN and self.located_mines[yn][xn] == MINE:
							place = MINE
						unsearched.append([yn, xn, place])
				
			# zaradi mezi prohledane
			searched.append(coord)
			if 0 and DEBUG:
				print("searched:", searched)
				print("unsearched:",unsearched)
		return searched
		
	# vyzkousi dosadit vsechny kombinace
	# zaznamena si vsechny mozne validni kombinace a vybere si ty pozice, ktere v zadnem z pripadu neobsahovaly minu.
	# mohl by si zaznamavat v kolika pripadech tam ta mina byla. Po te zahrat na pozici s nejnizsi pravdepodobnosti.
	def FindValidCombinations (self, data):
		#data = [Y_size, X_size, min_y, min_x, sandbox, unknown_coords, mine_coords]
		Y_size = data[0] 
		X_size = data[1]
		min_y = data[2]
		min_x = data[3]
		sandbox = data[4]
		unknown_coords = data[5]
		mine_coords = data[6]
		
		# navratova hodnota
		ret_coords = copy.deepcopy(unknown_coords)
		# nastavi pocet nalezenych min na nulu
		for coord in ret_coords:
			coord[2] = 0
		
		# vytvorit kombinace min pro tyto pozice (0-n min)
		kombination = Kombination(len(unknown_coords), 2)
		while (True != False):
			# vytvori nove pokusne pole 
			board = self.MakeFreeBoard(Y_size, X_size)
			# nakopiruje zname miny
			for coord in mine_coords:
				y = coord[0]
				x = coord[1]
				value = coord[2]
				board[y-min_y][x-min_x] = value
			
			# posune se na dalsi kombinaci
			komb = kombination.Next()
			if komb == None:		# vyzkouseli jsme vsechny kombinace
				print("Konec kombinacím!")
				break
			# zmeni obsah unknown na kombinaci
			for i in range(len(unknown_coords)):
				coord = unknown_coords[i]
				coord[2] = komb[i]
			
			# nakopiruje kombinaci na pozice
			for coord in unknown_coords:
				y = coord[0]
				x = coord[1]
				value = coord[2]
				board[y-min_y][x-min_x] = value
			
			# vyplni okolni cisla, vygeneruje novou desku
			self.CalculateNumbers(board)
			
			if 0 and DEBUG:
				Player.PrintBoard(board)
				print("Kombinace: ", komb)
				input()
			
			# porovnat s originalem
			if self.BoardsAreMatch(sandbox, board, Y_size, X_size):
				if DEBUG:
					Player.PrintBoard(board)
					print("Kombinace: ", komb)
					#input()
				
				# pri uplne shode zaznamenat polohu min, ktere sousedi puvodne odhalenymi cisli.
				for i in range(len(unknown_coords)):
					if unknown_coords[i][2] == MINE:
						ret_coords[i][2] = ret_coords[i][2] +1
			
		return ret_coords
	
	# pokusi se to umlatit pres kombinace
	def SolveByTry (self):
		# Rozdelit na podsektory
		# hleda neznamou pozici
		coords = self.FindUnknown()
		if DEBUG:
			print("Unknown coords:", coords)
		
		# Z ni spousti floodfill, ktery obsahuje neznama pole, miny a konci na cislech. Do vyhledavani pridava i cisla, ktera maji miny mimo jiz prohledanou oblast. Vrati sekvenci souradnic poli k vykopirovani
		area_coords = self.FloodFill(coords[0])
		
		# vytvorit vyrez
		# cropp = [min_y, max_y, min_x, max_x]
		cropp = self.FindCropp(area_coords) 
		min_y = cropp[0]
		max_y = cropp[1]
		min_x = cropp[2]
		max_x = cropp[3]
		if DEBUG:
			print("Cropp: y:", min_y, max_y, "x:", min_x, max_x)
		
		# alokovani pameti
		Y_size = max_y - min_y +1
		X_size = max_x - min_x +1
		sandbox = self.MakeFreeBoard(Y_size, X_size)
		print("Y,X:",len(sandbox), len(sandbox[0]))
			
		# nakopirovat podsektory i s nalezenymi minami do vlastniho sendboxu, posune podle vyrezu
		mine_coords = []
		unknown_coords = []
		for coord in area_coords:
			y = coord[0]
			x = coord[1]
			value = coord[2]
			#print(y-min_y, x-min_x)
			sandbox[y-min_y][x-min_x] = value
			# oznaci vsechny zname miny
			if value == MINE:
				mine_coords.append(coord)
			# oznacit vsechny nezname pozice
			if value == UNKNOWN:
				# pokud sousedi s cislem, tak neni jeho hodnota irelevantni
				if len(self.FindNumbersAround(y, x)) > 0:
					unknown_coords.append(coord)
		
		if len(unknown_coords) > self.max_unknown:
			print("Prilis mnoho moznych kombinaci.")
			return None
		
		if DEBUG:
			Player.PrintBoard(sandbox)
		
		# vytvorit kombinace min pro tyto pozice (0-n min)
		# pole kombinations obsahuje souradnice neznamych pozic a pocet vyskytu min.
		
		data = [Y_size, X_size, min_y, min_x, sandbox, unknown_coords, mine_coords]
		combinations = self.FindValidCombinations(data)
		if DEBUG:
			print("Kombinace min:", combinations)
			input()	
		
		# najde nejnizsi vyskyt min mezi vsemi neznamimi poli
		min_number = combinations[0][2]		# default
		max_number = 0
		for coord in combinations:
			if coord[2] < min_number:
				min_number = coord[2]
			elif coord[2] > max_number:
				max_number = coord[2]
				
		if max_number == 0:
			# pokud ve vsech pripadech tam mina nebyla, tak tyto pozice zaradi na listinu next.
			for coord in combinations:
				y = coord[0]
				x = coord[1]
				self.next_to_clear.append([y,x])
		else: 
			# TODO
			# tady se to da jiste nejak optimalizovat
			trehold = 1
			if min_number > trehold:
				coord = random.choice(combinations)
				y = coord[0]
				x = coord[1]
				self.next_to_clear.append([y,x])
			
			else:
				for coord in combinations:
					if coord[2] == min_number:
						y = coord[0]
						x = coord[1]
						self.next_to_clear.append([y,x])
		
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
						if self.IsBoard(self.Y, self.X, yn, xn) and self.board[yn][xn] == UNKNOWN:
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
		number_free = len(Player.Find(self.board, FREE))
		if len(self.next_to_clear) == 0 and number_free > self.min_free:
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
			
	def PrintBoard(board):
		Y = len(board)
		X = len(board[0])
		
		print(" --- Board ---")
		for y in range(Y):
			for x in range(X):
				if board[y][x] == UNKNOWN:
					print("#", end='')
				elif board[y][x] == FREE:
					print("_", end='')
				elif board[y][x] == MINE:
					print("x", end='')
				else:
					print(board[y][x], end='')
			print()
	
"""	
	# jsou to validni souradnice?
	def IsBoard (self, y, x):
		if (y >= 0 and y < self.Y and x >= 0 and x < self.X):
			return True
		return False
END
"""