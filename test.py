# By Pytel
"""
Slouzi k testovani validity funkci v Game.py a AI.py
"""

import Game
import AI

number = 20
X = 16
Y = 8

game = Game.Game(number, Y, X)
player = AI.Player(Y, X)
game.NewGame()
#game.PrintMines()
#game.Print()

"""
 --- Mines ---
 ___112112x21x1__
 ___1x2x23x2111__
 1111244x211_____
 1x112xx21_______
 1234x531_111_111
 _1xxxx1_12x1_2x2
 122332212x21_2x2
 x1____1x211__111
"""
board = [
[None, None, None, None, None, None, None, 1, 2, None, 2, 1, None, 1, None, 0],
[None, None, None, None, None, None, None, 2, 3, None, 2, 1, 1, 1, 0, 0],
[None, None, None, None, None, None, 4, None, 2, 1, 1, 0, 0, 0, 0, 0],
[None, None, None, None, None, None, None, 2, 1, 0, 0, 0, 0, 0, 0, 0],
[1, 2, 3, None, None, 5, 3, 1, 0, 1, 1, 1, 0, 1, 1, 1], 
[0, 1, None, None, None, None, 1, 0, 1, 2, None, 1, 0, 2, None, 2],
[1, 2, 2, 3, 3, 2, 2, 1, 2, None, 2, 1, 0, 2, None, 2],
[None, 1, 0, 0, 0, 0, 1, None, 2, 1, 1, 0, 0, 1, 1, 1]]


game.board = board
game.Print()
"""
 --- Game board ---
 #######12#21#1__
 #######23#2111__
 ######4#211_____
 #######21_______
 123##531_111_111
 _1####1_12#1_2#2
 122332212#21_2#2
 #1____1#211__111
"""

move = player.Move(game.GetBoard())
game.Execute(move)
move = player.Move(game.GetBoard())
print("Move:", move)

"""
if __name__ == '__main__':
	import doctest
	doctest.testmod() 

END
"""