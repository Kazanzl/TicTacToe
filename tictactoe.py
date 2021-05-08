"""
Tic Tac Toe Player
"""
import math
import copy
import random

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    players = [X, O]

    #calculate how many empty cells on the board
    empty_cells = sum(row.count(EMPTY) for row in board)
    
    if not empty_cells:
        return None

    #return the player depending on number of empty cells
    return players[(empty_cells-1) % 2]
            
def actions(board):
    possibleMoves = set()
    no_of_cols = len(board[0])
    no_of_rows = no_of_cols
    for row in range(no_of_rows):
        for col in range(no_of_cols):
            if not board[row][col]:
                possibleMoves.add((row, col))
    return possibleMoves

def result(board, action):
    i, j = action
    #check whether the cell is empty or not
    try:
        filled_cell = board[i][j]
        if filled_cell:
            raise Exception('Cell is already filled.')
    except IndexError:
        print('Invalid move.')

    #create deep copy of original board so that minimax does not affect original configuration
    boardcopy = copy.deepcopy(board)
    boardcopy[i][j] = player(boardcopy)
    return boardcopy

def winner(board):
    no_of_cols = len(board[0])
    no_of_rows = no_of_cols
    for i in range(no_of_cols):
        current_cell = board[0][i]
        if not current_cell:
            continue

        if i == 0:
            for j in range(1, no_of_rows):
                if board[j][j] != current_cell:
                    break
            else:
                return current_cell

        if i == no_of_cols - 1:
            for j in range(1, no_of_rows):
                if board[j][i-j] != current_cell:
                    break
            else:
                return current_cell

        for j in range(1, no_of_rows):
            if board[j][i] != current_cell:
                break
        else:
            return current_cell
    
    for j in range(no_of_rows):
        current_cell = board[j][0]
        for i in range(1, no_of_cols):
            if board[j][i] != current_cell:
                break
        else:
            return current_cell

    return None

def terminal(board):
    victor = winner(board)
    if victor or (not victor and not player(board)):
        return True
    return False

def utility(board):
    value = {'O': -1, None: 0, 'X': 1}
    victor = winner(board)
    return value[victor]

def minimax(board):
    if terminal(board):
        return None
    actingPlayer = player(board)
    if actingPlayer == 'X':
        bestVal, bestMove, minSteps = maxValue(board)
    else:
        bestVal, bestMove, minSteps = minValue(board)
    return bestMove

def maxValue(board, alpha=-math.inf, beta=math.inf, steps=0):
    if terminal(board):
        return (utility(board), None, steps)
    
    minSteps = math.inf
    bestVal = -math.inf
    bestMove = None
    validActions = actions(board)
    for action in validActions:
        resulted_board = result(board, action)
        actionVal, move, num_of_steps = minValue(resulted_board, alpha, beta, steps+1)
        if actionVal > bestVal:
            bestVal = actionVal
            bestMove = action
        elif actionVal == bestVal and num_of_steps < minSteps:
            bestVal = actionVal
            bestMove = action
            minSteps = num_of_steps

        alpha = max(alpha, actionVal)
        if beta <= alpha:
            break
    return (bestVal, bestMove, minSteps)

def minValue(board, alpha=-math.inf, beta=math.inf, steps=0):
    if terminal(board):
        return (utility(board), None, steps)
    
    minSteps = math.inf
    bestVal = math.inf
    bestMove = None
    validActions = actions(board)
    for action in validActions:
        resulted_board = result(board, action)
        actionVal, move, num_of_steps = maxValue(resulted_board, alpha, beta, steps+1)
        if actionVal < bestVal:
            bestVal = actionVal
            bestMove = action
        elif actionVal == bestVal and num_of_steps < minSteps:
            bestVal = actionVal
            bestMove = action
            minSteps = num_of_steps

        beta = min(beta, actionVal)
        if beta <= alpha:
            break
    return (bestVal, bestMove, minSteps)

