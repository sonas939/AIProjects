import copy

class Board:
    def __init__(self,pruning=False):
        self.grid = [['.' for i in range(3)]for j in range(3)]
        self.node = 0
        self.poss_actions = []
        self.pruning = pruning

    '''print tic-tac-toe board'''
    def __repr__(self):
        s = ""
        for i in self.grid:
            for j in i:
                s += j + " "
            s += '\n'
        return s
    
    '''returns whether game has finished (no empty spots or player/opponent has won'''
    def is_terminal(self,state):
        empty = False
        for i in range(3):
            if state[i][0] == "." or state[i][1] == "." or state[i][2] == ".":
                empty = True
                continue
            if state[i][0] == state[i][1] == state[i][2]:
                return True
            if state[0][i] == state[1][i] == state[2][i]:
                return True
        if state[0][0] == state[1][1] == state[2][2] and state[0][0] != ".":
            return True
        if state[0][2] == state[1][1] == state[2][0] and state[0][2] != ".":
            return True
        return not empty
    
    '''returns the utility value for terminal state'''
    def utility(self,state,player,depth):
        for i in range(3):
            if state[i][0] == state[i][1] == state[i][2]:
                if state[i][0] == player:
                    return 1 - 0.1 * depth
                else:
                    return -1 + 0.1 * depth
            if state[0][i] == state[1][i] == state[2][i]:
                if state[0][i] == player:
                    return 1 - 0.1 * depth
                else:
                    return -1 + 0.1 * depth
        if state[0][0] == state[1][1] == state[2][2]:
            if state[0][0] == player:
                return 1 - 0.1 * depth
            else:
                return -1 + 0.1 * depth
        if state[0][2] == state[1][1] == state[2][0]:
            if state[0][2] == player:
                return 1 - 0.1 * depth
            else:
                return -1 + 0.1 * depth
        #else means there is a draw
        return 0
    
    '''returns a copy of state with action'''
    def result(self,state,action,player):
        r = ord(action[0])-65
        c = int(action[1])-1
        newState = copy.deepcopy(state)
        newState[r][c] = player
        return newState
        
    '''returns list of all possible actions from given state'''
    def actions(self,state):
        actions = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == ".":
                    actions.append((chr(i+65),j+1))
        return actions
    
    '''returns min value'''
    def min_value(self,state,player,opponent,alpha=0,beta=0,depth=0):
        if self.is_terminal(state):
            return self.utility(state,player,depth-1),None
        self.node += 1
        v = float('inf')
        move = ""
        for a in self.actions(state):
            v2,a2 = self.max_value(self.result(state,a,opponent),player,opponent,alpha,beta,depth+1)
            if v2 < v:
                v,move = v2,a
                if self.pruning:
                    beta = min(beta,v)
            if self.pruning:
                if v <= alpha:
                    return v,move
        return v,move
    
    '''returns max value'''
    def max_value(self,state,player,opponent,alpha=0,beta=0,depth=0):
        if self.is_terminal(state):
            return self.utility(state,player,depth-1),None
        self.node += 1
        v = float('-inf')
        move = ""
        for a in self.actions(state):
            v2,a2 = self.min_value(self.result(state,a,player),player,opponent,alpha,beta,depth+1)
            if depth == 0:
                self.poss_actions.append([a,v2])
            if v2 > v:
                v,move = v2,a
                if self.pruning:
                    alpha = max(alpha,v)
            if self.pruning:
                if v >= beta:
                    return v,move
        return v,move

    '''user fills in grid'''
    def move(self,p,r,c):
        row = 0
        if r == "B":
            row = 1
        elif r == "C":
            row = 2
        if self.grid[row][c-1] == ".":
            self.grid[row][c-1] = p
        else:
            print("Piece already at position")
    
    '''use minimax to fill in grid'''
    def choose(self,state,player):
        opponent = "X"
        if player == "X":
            opponent = "O"
        value,move = self.max_value(state,player,opponent,float('-inf'),float('inf'),0)
        r = ord(move[0])-65
        c = int(move[1])-1
        self.grid[r][c] = player


def main():
    board = Board()
    print("Welcome to Tic-Tac-Toe")
    print(board)
    usrIn = input("> ").split(" ")
    while usrIn[0] != "quit":
        if usrIn[0] == "show":
            print(board)
        elif usrIn[0] == "reset":
            board = Board()
            print("The board has been reset.")
            print(board)
        elif usrIn[0] == "move":
            board.move(usrIn[1],usrIn[2],int(usrIn[3]))
            print(board)
        elif usrIn[0] == "choose":
            board.choose(board.grid,usrIn[1])
            for i in board.poss_actions:
                print("move ({},{}) mm-score: {}".format(i[0][0],i[0][1],"{:.1f}".format(round(i[1],2))))
            print("number of nodes searched: {}".format(board.node))
            board.poss_actions = []
            board.node = 0
            print(board)
        elif usrIn[0] == "pruning":
            if len(usrIn) == 1:
                if board.pruning:
                    print("pruning=1"+'\n')
                else:
                    print("pruning=0"+'\n')
            elif usrIn[1].lower() == "on":
                board.pruning = True
                print("pruning=1 \n")
            elif usrIn[1].lower() == "off":
                board.pruning = False
                print("pruning=0 \n")
            else:
                print("Invalid Input"+'\n')
        else:
            print("Invalid Input"+'\n')
        if board.is_terminal(board.grid):
            num = board.utility(board.grid,'X',0)
            if num > 0:
                print("*** X wins! ***")
            elif num < 0:
                print("*** O wins! ***")
            else:
                print("*** it's a draw! ***")
            print("Board has been reset. Type quit to exit the game. \n")
            board = Board()
        usrIn = input("> ").split(" ")


if __name__ == "__main__":
    main()