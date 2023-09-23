Dark Matter MiniGolf
Dependencies:
1. pygame
2. pymunk

Building the game:
Once you have unzipped the files, make sure you have both pygame and pymunk installed on your
python path, then run the run_game.py file.

Controls:
Clickling the mouse will apply an impulse to the golf ball. The direction of that impulse
(i.e., x/y directions) are determined by the position of the mouse. The arrow always points
towards the mouse and moves with the ball, but it does not rotate around the ball. As a result,
you want to use the arrow's angle to determine where you're hitting the ball, not it's relative
position to the ball.

Features:
1. [1] minigolf course which allows you to hit a golf ball that bounces off the walls and stops at the hole.

All art resources sourced from Kenney at Kenney.nl under a CC0 license