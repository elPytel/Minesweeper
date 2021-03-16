#By Pytel
"""
Hra miny podle micr$ofti predlohy.
"""
import Game
import time
import AI

TIME = 1

number = 25
X = 16
Y = 8

"""
number = 3
X = 6
Y = 4
"""

game = Game.Game(number, Y, X)
player = AI.Player(Y, X)
game.NewGame()
game.PrintMines()
game.Print()

while game.IsEnd() == False:
	move = player.Move(game.GetBoard())
	print("Move:", move)
	valid = game.IsValidMove(move)
	if valid:
		if (game.Execute(move) == False):
			print("ERROR")
	else:
		print("ERROR: invalid move!")
		break
	game.Print()
	time.sleep(TIME)

print(" ---Game end ---")
print(" AI", "eploded!" if game.IsExploded() else "won!")
game.Print()

"""
Filtrování zbytečných polí ještě před ořezem.
Výpočet hodnot pole jen na těch relevantních místech.
END
"""