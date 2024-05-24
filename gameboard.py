#Defining BoardClass
import copy

class BoardClass:

    ''' This class represents all the necessary components 
    for tic-tac-toe, as well as the multiplayer components. 
    
    Attributes:
    User Name - tracks the username of each player
    Last Move User - denotes the player with the most recent move
    Player Piece - alternates depending on the player
    Rival Piece - alternates depending on the player 
    numWins - win count
    numTies - tie count
    numLosses - loss cout
    numGames - game count 
    TicTacToeBoard - sets up the board
    OriginalBoard - deep copies the original blank board 

    It also contains the functions that will run the game, as noted below.
    '''

    def __init__(self):
        self.userName = ''
        self.rivalName = ''
        self.lastMove = ''
        self.currentMove = ''
        self.playerPiece = ''
        self.rivalPiece = ''
        self.numWins = 0 
        self.numTies = 0 
        self.numLosses = 0 
        self.numGames = 0 
        self.TicTacToeBoard = [['_','_','_'],['_','_','_'],['_','_','_']]
        self.OriginalBoard = copy.deepcopy(self.TicTacToeBoard)


    ''' FUNCTIONS NEEDED 
    
    updateGamesPlayed() - updates numGames
    resetGameBoard() - resets TicTacToe to the original blank state 
    updateGameBoard() - continously updates the TTT Board
    isWinner() - checks win conditions (horizontal, vertical, diagonal)
    boardIsFull() - checks for ties 
    printStats - prints statistics for each player 
    printBoard() - prints board for every move
    playAgain - prompts the play again feature
    convertMove() - converts moves into x and y plane positions
    validateMove() - confirms valid move
    checkGameOver - confirms an end condition (tie, win, loss, etc.)
    '''

    def updateGamesPlayed(self): #KEEP TRACK OF HOW MANY GAMES HAVE STARTED
        self.numGames += 1

    def resetGameBoard(self): #CLEAR ALL MOVES FROM THE GAMEBOARD
        self.TicTacToeBoard = self.OriginalBoard
    
    def updateGameBoard(self, moveX, moveY, pieceType): #UPDATE GAME BOARD WITH PLAYER MOVES 
        self.TicTacToeBoard[moveX][moveY] = pieceType
        self.printBoard()
        
    def isWinner(self): #CHECKS LATEST MOVE FOR A WIN, UPDATES WIN AND LOSS COUNT
        b = self.TicTacToeBoard
        #check rows if rival won
        for row in range(0,3):
            if b[row][0] == b[row][1] == b[row][2] == self.rivalPiece:
                self.numLosses += 1
                return 'loss'
        #check rows if player won
        for row in range(0,3):
            if b[row][0] == b[row][1] == b[row][2] == self.playerPiece:
                self.numWins += 1
                return 'win'

        #check columns if rival won
        for col in range(0,3):
            if b[0][col] == b[1][col] == b[2][col] == self.rivalPiece:
                self.numLosses += 1
                return 'loss'
        #check columns if player won
        for col in range(0,3):
            if b[0][col] == b[1][col] == b[2][col] == self.playerPiece:
                self.numWins += 1
                return 'win'

        #check diagonals if rival won
        if b[0][0] == b[1][1] == b[2][2] == self.rivalPiece:
            self.numLosses += 1 
            return 'loss'
        
        if b[0][2] == b[1][1] == b[2][0] == self.rivalPiece:
            self.numLosses += 1 
            return 'loss'
        
        
        #check diagonals if player won
        if b[0][0] == b[1][1] == b[2][2] == self.playerPiece:
            self.numWins += 1 
            return 'win'
        if b[0][2] == b[1][1] == b[2][0] == self.playerPiece:
            self.numWins += 1 
            return 'win'
        
        return 'none'
        

    def boardIsFull(self): #CHECKS IF BOARD IS FULL (NO MORE MOVES, TIE)
        for row in self.TicTacToeBoard:
            for col in row:
                if col == '_':
                    return False
                        
        self.numTies += 1
        return True

    def printStats(self): #PRINTS PLAYER USERNAME, USERAME OF THE LAST PERSON TO MAKE A MOVE, NUMBER OF GAMES, # OF WINS, # OF LOSSES, # OF TIES
        print(f"Username: {self.userName}")
        print(f"Most Recent Move: {self.lastMove}")
        print(f"Games Played: {self.numGames}")
        print(f"Games Won: {self.numWins}")
        print(f"Games Lost: {self.numLosses}")
        print(f"Games Tied: {self.numTies}")

    def printBoard(self): #PRINTS BOARD
        for row in self.TicTacToeBoard: 
            print(' '.join(row))
        print()

    def playAgain(self):
        play = input("Play again? (Y/y or N/n): ")
        if play == 'y' or play == 'Y':
            return True
        return False
    
    def convertMove(self,move): #move is a str
        x = int(move.split(',')[0])
        y = int(move.split(',')[1])
        return x,y
    
    def validateMove(self,move):
        try:
            moves = self.convertMove(move)

            if len(moves) != 2: # bad input
                return False
            moveX = moves[0]
            moveY = moves[1]
            if moveX not in range(0,3): # bad range
                return False
            if moveY not in range(0,3): # bad range
                return False
            if self.TicTacToeBoard[moveX][moveY] != '_': # move already made
                return False
            
        except: #bad input
            return False
        
        return True

    def checkGameOver(self):
        #1. Check winner
        result = self.isWinner()
        if result == 'win':
            print('You are a winner!!!\n')
            return True
            
        elif result == 'loss':
            print('You are a loser!!!\n')
            return True

        else: #2. Check tie
            if (self.boardIsFull()):
                print("Tie game!!!\n")
                return True
        return False

        

if __name__ == "__main__":
    b = BoardClass()
    b.printBoard()
    b.printStats()