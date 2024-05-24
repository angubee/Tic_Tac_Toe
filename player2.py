import socket 
from gameboard import BoardClass

''' Player 2 is defaulted to be the server. This is the player that receives information and
is subject to what Player 1 decides. '''


def run_player2(): #SERVER
    socketPlayer2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True: 
        try: 
            #socketPlayer2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            IP_prompt = input("Input IP Address: \n")
            Port_prompt = int(input("Input Port Number: \n"))

            socketPlayer2.bind((IP_prompt, Port_prompt))
            print("Awaiting connection...")
            socketPlayer2.listen(1)
            
            server, player1Address = socketPlayer2.accept()
            print("Successful connection! Players are locked in.")

            break
        
        except:
            print("Invalid Host information. Please try again.")
            continue
        
    #connected
    GB = BoardClass()
    # Usernames
    print("Waiting for rival...")
    GB.rivalName = server.recv(1024).decode('ascii')
    print(f'Your rival is {GB.rivalName}\n')

    GB.userName = input("Please input your username: ")
    server.send(GB.userName.encode('ascii'))
    GB.playerPiece = 'O'
    GB.rivalPiece = 'X'

    #player 1 go first, so last move was technically player 2 ;)
    GB.currentMove = GB.rivalPiece
    print("Enter moves in this format: 'x,y' where x and y are in range 0-2")
    print("Beginning game!!!")
    GB.printBoard()

    '''This conducts the alternating of moves. This considers itself to the player
    and Player 1 to be its rival. Piece attributes alternate accordingly.'''

    # Begin game
    while(True):
        #Gameover or no
        if GB.checkGameOver():
            print("Asking rival if they want to play again, sorry :( you don't have a choice)")
            response = server.recv(1024).decode('ascii')
            if response == "Play Again":
                print("Run it back!\n")
                GB.resetGameBoard()
                GB.currentMove = GB.rivalPiece
                print("Enter moves in this format: 'x,y' where x and y are in range 0-2")
                print("Beginning game!!!")
                GB.printBoard()
                continue

            else:
                print("Fun times\n")
                print('Thanks for playing!')
                GB.printStats()
                break


        # player2 move
        if(GB.currentMove == GB.playerPiece):
            move = input("Input your move... ")
            # Check if move is valid and based
            while(GB.validateMove(move) != True):
                print("Invalid move, try again")
                move = input("Input your move... ")

            server.send(move.encode('ascii'))
            moveX,moveY = GB.convertMove(move)
            GB.updateGameBoard(moveX, moveY, GB.playerPiece)
            GB.lastMove = GB.userName
            # switch
            GB.currentMove = GB.rivalPiece
            continue

        # player1 move
        if(GB.currentMove == GB.rivalPiece):
            print("Waiting for rival's move...\n")
            move = server.recv(1024).decode('ascii')
            moveX, moveY = GB.convertMove(move)
            GB.updateGameBoard(moveX, moveY, GB.rivalPiece)
            GB.lastMove = GB.rivalName
            # switch
            GB.currentMove = GB.playerPiece
            continue
    
    print("Terminating!")
    server.close()

if __name__ == "__main__":
    run_player2()