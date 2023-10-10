
from distutils.command.install_lib import PYTHON_SOURCE_EXTENSION


board = ["-","-","-",
        "-","-","-",
        "-","-","-"]

currentPlayer = "X"
winner = None
gameRunning = True
def printboard(board):
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("----------")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("----------")
    print(board[6] + " | " + board[7] + " | " + board[8])

def playerinput(board):
    i=int(input("enter number 1-9:"))
    if i >= 1 and i <= 9 and board[i-1] == "-":
        board[i-1] = currentPlayer 
    else:
        print("Opps it is invalid")
        gameRunning = False
        return gameRunning
def horiozntalwin(board):
    global winner
    if (board[0]==board[1]==board[2] and board[0]!="-"):  
        winner = board[0]
        return True
    elif (board[3]==board[4]==board[5] and board[3]!="-"):
        winner = board[3]
        return True
    elif (board[6]==board[7]==board[8] and board[6]!="-") :
        winner =board[6]
        return True

def verticalwin(board):
    global winner
    if board[0]==board[3]==board[6] and board[0]!="-" :
        winner = board[0]
        return True
    elif board[1]==board[4]==board[7] and board[1]!="-":
        winner = board[1]
        return True
    elif board[2]==board[5]==board[8]!="-":
        winner = board[2]
        return True
    
def diagonalwin(board):
    global winner
    if board[0]==board[4]==board[8] and board[0]!="-" : 
        winner = board[0]
        return True
    elif board[2]==board[4]==board[6] and board[2]!="-":
        winner = board[2]
        return True
def Tie(board):
    global gameRunning
    if "-" not in board :
        printboard(board)
        print("It is Tie")
        gameRunning=False
def switch_player():
    global currentPlayer
    if currentPlayer == "X":
        currentPlayer = "O"
    else:
        currentPlayer = "X"
    return currentPlayer

def Checkwin(board):
    global gameRunning
    if diagonalwin(board) or verticalwin(board) or horiozntalwin(board):
        print(f"The winner is {winner}")
        gameRunning = False
import random
def computer(board):
    if currentPlayer =="O":
        position=random.randint(0,8)
        if board[position]=="-":
            board[position]="O"
    switch_player()

while gameRunning == True:
    printboard(board)
    playerinput(board)
    Checkwin(board)
    Tie(board)
    switch_player()
    computer(board)
    Checkwin(board)
    Tie(board)
    switch_player()