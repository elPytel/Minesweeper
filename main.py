#By Pytel
"""
Hra miny podle micr$ofti predlohy.
"""
import Game
import time
import AI

number = 20
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
	time.sleep(2)

print(" ---Game end ---")
print(" AI", "eploded!" if game.IsExploded() else "won!")
game.Print()

"""
END
"""