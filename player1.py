import socket 
from gameboard import BoardClass 

''' Player 1 is defaulted to be the client. This is the player that controls whether a game 
continues or not, as well as the connections.'''

def run_player1(): #CLIENT 

    '''Does initial attempts to connect the socket, and if it fails
    attempts to refresh socket and continuously tries to connect with Player 2 (the server).'''
    
    while True: 
        try: 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            IP_prompt = input("Input IP Address: \n")
            Port_prompt = int(input("Input Port Number: \n"))

            client.connect((IP_prompt, Port_prompt))
            print("Successful connection! Players are locked in.")
            break

        except:
            error_prompt = input("Connection cannot be made. Type 'Y' to try again, 'N' to exit. ")
            if error_prompt == 'Y' or error_prompt == 'y':
                continue 
            else:
                print("Goodbye!")
                quit()


    #connected, initialized class
    GB = BoardClass()
    # Usernames
    #UNCOMMENT
    GB.userName = input("Please input your username: ")
    client.send(GB.userName.encode('ascii'))

    print("Waiting for rival...")
    GB.rivalName = client.recv(1024).decode('ascii')
    print(f'Your rival is {GB.rivalName}\n')
    # Assign piece
    GB.playerPiece = 'X'
    GB.rivalPiece = 'O'

    #player 1 go first, so last move was technically player 2 ;)
    GB.currentMove = GB.playerPiece
    print("Enter moves in this format: 'x,y' where x and y are in range 0-2")
    print("Beginning game!!!")
    GB.printBoard()

    '''Conducts the alternating of moves, this is the player and considers 
    P2 the rival. Piece attributes alternate accordingly.'''

    # Begin game
    while(True):
        #Gameover or no
        if GB.checkGameOver():
            playon = GB.playAgain()
            if playon:
                #play again
                print("Let's go again! Sending to rival")
                playMessage = "Play Again"
                client.send(playMessage.encode('ascii'))
                print("Playing again!")

                GB.currentMove = GB.playerPiece
                print("Enter moves in this format: 'x,y' where x and y are in range 0-2")
                GB.resetGameBoard()
                print("Beginning game!!!")
                GB.printBoard()
                continue
                

            else:
                print('Fun times\n')
                print('Thanks for playing!')
                GB.printStats()
                break


        # player2 move
        if(GB.currentMove == GB.rivalPiece):
            print("Waiting for rival's move...\n")
            move = client.recv(1024).decode('ascii')
            moveX, moveY = GB.convertMove(move)
            GB.updateGameBoard(moveX, moveY, GB.rivalPiece)
            GB.lastMove = GB.rivalName
            # switch
            GB.currentMove = GB.playerPiece
            continue


        # player1 move
        if(GB.currentMove == GB.playerPiece):
            move = input("Input your move... ")
            # Check if move is valid and based
            while(GB.validateMove(move) != True):
                print("Invalid move, try again")
                move = input("Input your move... ")

            client.send(move.encode('ascii'))
            moveX,moveY = GB.convertMove(move)
            GB.updateGameBoard(moveX, moveY, GB.playerPiece)
            GB.lastMove = GB.userName
            # switch
            GB.currentMove = GB.rivalPiece
            continue


    print("Terminating!")
    client.close()






if __name__ == "__main__":
    run_player1()