from hashlib import new
import math
import os
import random
import re
import sys
import copy

def encoder(p1, board) :
    power, number = 0, 0
    for i in range(3):
        for j in range(3) :
            # print(f"Power = {power}")
            if board[i][j] == 'X' :
                number += (1*(3**power))
            elif board[i][j] == 'O' :
                number += (2*(3**power))
            power += 1
    if p1 == 'X' : number += (1*(3**9))
    else : number += (2*(3**9))
    
    # print(f"Player : {p1} Number : {number}")
    return (number)

def decoder(number) :
    dboard = [['_' for j in range(3)] for i in range(3)]
    # print()
    # print(f"Board : {dboard}")
    for i in range(3):
        for j in range(3) :
            # print(f"i = {i} j = {j} Number % 3 = {number % 3}")
            if number % 3 == 1 : 
                dboard[i][j] = 'X' 
            elif number % 3 == 2 : 
                dboard[i][j] = 'O' 
            number //= 3
            # print(f"Number // 3 = {number}")
            # print(f"Board : {dboard}")
    
    if number % 3 == 1 : p = 'X'
    else : p = 'O'
    
    # print(f"Player : {p}")
    # print(f"Board : {dboard}")
    return(p, dboard)

def winCheck(ch, board) :
    row_win = any(all(board[i][j] == ch for j in range(3)) for i in range(3))
    col_win = any(all(board[i][j] == ch for i in range(3)) for j in range(3))
    pdia_win = all(board[i][i] == ch for i in range(3))
    odia_win = all(board[i][2 - i] == ch for i in range(3))
    
    return any([row_win , col_win , pdia_win , odia_win])

def isGameOver(board) :
    
    win_x =  winCheck('X', board)
    win_o =  winCheck('O', board)
    
    isFull = not any(emptyPos(board))
    
    if win_x:
        return (True, 'X')
    elif win_o:
        return (True, 'O')
    elif isFull:
        return (True, '_')
    else:
        return (False, '_')

def emptyPos(board) :
    return ((i , j) for j in range(3) for i in range(3) if board[i][j] == '_')

def flip_player(p1):
    return 'O' if p1 == 'X' else 'X'

def print_board(board):
    for i in range(3):
        for j in range(3):
            print(board[i][j], end=' ')
        print()
    print()

def scoreMove(main_player, n, choice) :
    global board_dict , board_dict1
    player, state = decoder(n)
    if choice == 1 or player == main_player :
        if n in board_dict :
            return board_dict[n]
    else :
        if n in board_dict1 :
            return board_dict1[n]
    
    gameOver, winner = isGameOver(state)
    score = 0
    if gameOver:
        if player == winner:
            score = 1 if player == main_player else -1
        elif winner == '_':
            score = 0
        else:
            score = -1 if player == main_player else 1
    else:
        scores = []
        for pos in emptyPos(state):
            new_board = state
            change = new_board[pos[0]][pos[1]]
            new_board[pos[0]][pos[1]] = player
            s = scoreMove(main_player, encoder(flip_player(player),new_board), choice)
            scores.append(s)
            new_board[pos[0]][pos[1]] = change
        
        if main_player == player :
            score = max(scores)
        else :
            score = min(scores)
    # print(score)
    # print_board(board)
    if choice == 1 or player == main_player:
        board_dict.update({n : score})
    else :
        board_dict1.update({n : score})
    
    return score

def nextMove(p1, board, choice):
    n = encoder(p1, board)
    player, state = decoder(n)
    scores = []
    max_score = -math.inf
    arg_max_score = None
    scores = []
    for pos in emptyPos(state):
        new_board = state
        change = new_board[pos[0]][pos[1]]
        new_board[pos[0]][pos[1]] = player
        score = scoreMove(player, encoder(flip_player(player), new_board), choice)
        scores.append((score, pos))
        new_board[pos[0]][pos[1]] = change
        max_score = max(score, max_score)
    max_scores = list((s, pos) for s, pos in scores if s == max_score)
    arg_max_score = random.sample(max_scores, 1)[0][1]
    return arg_max_score            
            
def printResult(p1, board, choice):
        gameOver, winner = isGameOver(board)
        if gameOver:
            if winner == p1:
                print(f"Congratulations {p1} Won!!")
            elif winner == '_':
                print("It's a draw. Well played!!")
            else:
                if choice != 2 :
                    print(f"Computer {flip_player(p1)} Won!. Try again. Sorry!!")
                else :
                    print(f"Player {flip_player(p1)} Won!!")
        return gameOver

if __name__ == '__main__':
    
    board_dict , board_dict1 = dict() , dict()
    board = [['_' for j in range(3)] for i in range(3)]
    
    print("Welcome to the game of Tic Tac Toe")
    print(f"Select any one of the following :\n1. Player Vs Comp\n2. Player Vs Player\n3. Comp Vs Comp\n Enter your choice : ", end = '')
    choice = int(input())
    print()
    
    if choice == 1 :
        print(f"Player Vs Comp\n")
        print("Select a player: ('X' or 'O')")
        p1 = input()
        assert p1 == 'X' or p1 == 'O'
        # print(board)
        gameOver = False
        while not gameOver:
            print(f"Make your move player {p1}: (Enter coordinates)")
            right_move = False
            move = None
            while not right_move:
                move = [int(i) for i in input().split(' ')]
                if tuple(move) in emptyPos(board):
                    right_move = True
                else:
                    print("Enter a valid position")
            board[move[0]][move[1]] = p1
            print_board(board)
            gameOver = printResult(p1, board, choice)
            if gameOver:
                break
            print("Comp making the move...")        
            move2 = nextMove(flip_player(p1), board, choice)
            print(f"Comp moves on {move2}")
            board[move2[0]][move2[1]] = flip_player(p1)
            print_board(board)
            gameOver = printResult(p1, board, choice)
            if gameOver:
                break
        
    elif choice == 2 :
        print(f"Player Vs Player\n")
        print("Select a player 1 : ('X' or 'O')")
        p1 = input()
        assert p1 == 'X' or p1 == 'O'
        p2 = flip_player(p1)
        
        gameOver = False
        while not gameOver:
            print(f"Make your move player {p1}: (Enter coordinates)")
            right_move = False
            move = None
            while not right_move:
                move = [int(i) for i in input().split(' ')]
                if tuple(move) in emptyPos(board):
                    right_move = True
                else:
                    print("Enter a valid position")
            board[move[0]][move[1]] = p1
            print_board(board)
            gameOver = printResult(p2, board, choice)
            if gameOver:
                break
            print(f"Make your move player {p2}: (Enter coordinates)")
            right_move = False
            move = None
            while not right_move:
                move = [int(i) for i in input().split(' ')]
                if tuple(move) in emptyPos(board):
                    right_move = True
                else:
                    print("Enter a valid position")
            board[move[0]][move[1]] = p2
            print_board(board)
            gameOver = printResult(p1, board, choice)
            if gameOver:
                break
        
    elif choice == 3 :
        print(f"Comp Vs Comp\n")
        p_list = ['X' , 'O']
        p1 = random.choice(p_list)
        # print(board)
        gameOver = False
        while not gameOver:
            print(f"Comp 1 {p1} making the move...")        
            move = nextMove(p1, board, choice)
            print(f"Computer moves on {move}")
            board[move[0]][move[1]] = p1
            print_board(board)
            gameOver = printResult(p1, board, choice)
            if gameOver:
                break
            print(f"Comp 2 {flip_player(p1)} making the move...")        
            move2 = nextMove(flip_player(p1), board, choice)
            print(f"Computer moves on {move2}")
            board[move2[0]][move2[1]] = flip_player(p1)
            print_board(board)
            gameOver = printResult(p1, board, choice)
            if gameOver:
                break
            
    else :
        print(f"Not a valid choice!\n")