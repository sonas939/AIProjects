Command to run program: python3 ttt.py

Available commands once running program:
- show: see current state of board
- reset: resets board to default (empty board)
- move P R C: P can be X or O, R is the valid row (A,B,C), and C is the valid column (1,2,3). Please P in spot specified by R and C.
- choose P: P can be X or O. Invokes Minimax to figure out optimal spot to place P
- pruning: shows if pruning is on or off
- pruning on: turns alpha-beta pruning on
- pruning off: turns alpha-beta pruning off
- quit: exits out of program

Please note that basic error checking has been implemented (i.e. if a non-valid command is entered, "Invalid Output" will be printed). However, this is the extent of the error checking. 