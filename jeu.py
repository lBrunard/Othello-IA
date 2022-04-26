import copy
from sre_parse import State
import time
import random

from cborad import board

def timeit(fun):
	def wrapper(*args, **kwargs):
		start = time.time()
		res = fun(*args, **kwargs)
		print('Executed {} in {}s'.format(fun, time.time() - start))
		return res
	return wrapper

directions = [
    ( 0,  1),
    ( 0, -1),
    ( 1,  0),
    (-1,  0),
    ( 1,  1),
    (-1,  1),
    ( 1, -1),
    (-1, -1)
]

def add(p1, p2):
    l1, c1 = p1
    l2, c2 = p2
    return l1 + l2, c1 + c2

def coord(index):
    return index // 8, index % 8

def index(coord):
    l, c = coord
    return l*8+c

def isInside(coord):
    l, c = coord
    return 0 <= l < 8 and 0 <= c < 8

def walk(start, direction):
    current = start
    while isInside(current):
        current = add(current, direction)
        yield current

def isGameOver(state):
    playerIndex = state['current']
    otherIndex = (playerIndex+1)%2

    res = False
    if len(possibleMoves(state)) == 0:
        state['current'] = otherIndex
        if  len(possibleMoves(state)) == 0:
            res = True
    state['current'] = playerIndex
    return res

def willBeTaken(state, move):
    playerIndex = state['current']
    otherIndex = (playerIndex+1)%2

    if not (0 <= move < 64):
        raise "Not in board"#raise game.BadMove('Your must be between 0 inclusive and 64 exclusive')

    if move in state['board'][0] + state['board'][1]:
        raise "Case not free"#raise game.BadMove('This case is not free')

    board = []
    for i in range(2):  
        board.append(set((coord(index) for index in state['board'][i])))

    move = coord(move)

    cases = set()
    for direction in directions:
        mayBe = set()
        for case in walk(move, direction):
            if case in board[otherIndex]:
                mayBe.add(case)
            elif case in board[playerIndex]:
                cases |= mayBe
                break
            else:
                break

    if len(cases) == 0:
        raise "Not takable place"#raise game.BadMove('Your move must take opponent\'s pieces')
    
    return [index(case) for case in cases]

def possibleMoves(state):
    res = []
    for move in range(64):
        try:
            willBeTaken(state, move)
            res.append(move)
        except :#game.BadMove:
            pass
    return res


def Othello(players):
    # 00 01 02 03 04 05 06 07
    # 08 09 10 11 12 13 14 15
    # 16 17 18 19 20 21 22 23
    # 24 25 26 27 28 29 30 31
    # 32 33 34 35 36 37 38 39
    # 40 41 42 43 44 45 46 47
    # 48 49 50 51 52 53 54 55
    # 56 57 58 59 60 61 62 63

    state = {
        'players': players,
        'current': 0,
        'board': [
            [28, 35],
            [27, 36]
        ]
    }

    def next(state, move):
        newState = copy.deepcopy(state)
        playerIndex = state['current']
        otherIndex = (playerIndex+1)%2

        if len(possibleMoves(state)) > 0 and move is None:
            raise ("Impossible")#game.BadMove('You cannot pass your turn if there are possible moves')

        if move is not None:
            cases = willBeTaken(state, move)

            newState['board'][playerIndex].append(move)

            for case in cases:
                newState['board'][otherIndex].remove(case)
                newState['board'][playerIndex].append(case)
            
        newState['current'] = otherIndex

        # if isGameOver(newState):
        #     if len(newState['board'][playerIndex]) > len(newState['board'][otherIndex]):
        #         winner = playerIndex
        #     elif len(newState['board'][playerIndex]) < len(newState['board'][otherIndex]):
        #         winner = otherIndex
        #     else:
        #         print("Draw")#game.GameDraw(newState)
        #     print("WINNER")#game.GameWin(winner, newState)
        
        return newState

    return state, next

def winner(state):
    if len(state["board"][0]) > len(state["board"][1]):
        return 0
    return 1
    
def currentPlayer(state):
    if state["board"][0] < state["board"][1]:
        return 0 , 1
    else:
        return 1 , 0
    
# Coin Parity Heuristic Value =
# 100* (Max Player Coins –Min Player Coins)/
# (Max Player Coins + Min Player Coins)
def heuristic(state, player):
    currentP = state["board"][currentPlayer(state)[0]]
    otherP = state["board"][currentPlayer(state)[1]]
    return 100*(len(currentP) - len(otherP))/(len(currentP) + len(otherP))

def negamaxWithPruningLimitedDepth(state, player, depth=4, alpha=float('-inf'), beta=float('inf')):
    if isGameOver(state) or depth == 0:
        return -heuristic(state, player), None

    theValue, theMove = float('-inf'), None
    moves = possibleMoves(state)
    for move in moves:
        successor = next(state, move)
        value, _ = negamaxWithPruningLimitedDepth(successor, player%2+1, depth-1, -beta, -alpha)
        if value > theValue:
            theValue, theMove = value, move
            alpha = max(alpha, theValue)
        if alpha >= beta:
            break
    return -theValue, theMove

@timeit
def negamaxWithPruning(state, player, alpha=float('-inf'), beta=float('inf')):
    if isGameOver(state):
        return -winner(state), None
    theValue, theMove = float('-inf'), None
    moves = possibleMoves(state)
    for move in moves:
        print('hello')
        successor = next(state, move)
        value,_ = negamaxWithPruning(successor, player%2+1, -beta, -alpha)
        if value > theValue:
            theValue, theMove = value, move
            alpha = max(alpha, theValue)
        if alpha >= beta:
            break
    return -theValue, theMove

@timeit
def next_branch(state, fct):
    player = currentPlayer(state)[0]
    _, move = fct(state, player)
    return move


def best_move(state):
    moves = possibleMoves(state)
    if len(moves) < 1:
        return None
    last_dif = 0
    best_array = []
    for move in moves:
        newState = next(state, move)
        dif = len(newState["board"][0]) - len(newState["board"][1])
        if dif > 0 and dif > last_dif:
            best_array = []
            best_array.append(move)
            last_dif = dif
        elif dif == last_dif:
            best_array.append(move)
    if not last_dif:
        return random.choice(moves)
    return random.choice(best_array)

Game = Othello

state, next = Game(['LUR', 'HSL'])
