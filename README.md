#**2048 pygame**

#**Getting Started**
1. Get Python 3.7+
2. Get pip, then install pygame
   $ pip install pygame
3. run the game
   $ python main.py

#**How to play this game?**
  1. Choose the theme and the difficulty then click play
  2. When you enter the game, 2048 is played on a gray 4×4 grid, with numbered tiles that slide when a player moves them using the four arrow keys or W A S D.
  3. There are some features for you to type like: (U)Undo, (N)Restart, (B)Backward, (Space)Paused/Resume, (Q)Quit
  4. Join the number togerther until it reach the difficulty you choose.
  5. There's also a replay option for you to choose (Y)Yes/(N)No.

#**Game rule!**
  1. Every turn, a new tile will randomly appear in an empty spot on the board with a value of either 2 or 4.
  2. Tiles slide as far as possible in the chosen direction until they are stopped by either another tile or the edge of the grid.
  3. If two tiles of the same number collide while moving, they will merge into a tile with the total value of the two tiles that collided.
  4. The resulting tile cannot merge with another tile again in the same move.
  5. If a move causes three consecutive tiles of the same value to slide together, only the two tiles farthest along the direction of motion will combine.
  6. If all four spaces in a row or column are filled with tiles of the same value, a move parallel to that row/column will combine the first two and last two.
