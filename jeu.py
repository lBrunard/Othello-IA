import copy
import time
import random
from collections import defaultdict
from threading import Thread
import game

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
        raise game.BadMove('Your must be between 0 inclusive and 64 exclusive')

    if move in state['board'][0] + state['board'][1]:
        raise game.BadMove('This case is not free')

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
        raise game.BadMove('Your move must take opponent\'s pieces')
    
    return [index(case) for case in cases]

def possibleMoves(state):
    res = []
    for move in range(64):
        try:
            willBeTaken(state, move)
            res.append(move)
        except game.BadMove:
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
            [28,35],
            [27,36]
        ]
    }

    def next(state, move):
        newState = copy.deepcopy(state)
        playerIndex = state['current']
        otherIndex = (playerIndex+1)%2

        if len(possibleMoves(state)) > 0 and move is None:
            raise game.BadMove('You cannot pass your turn if there are possible moves')

        if move is not None:
            cases = willBeTaken(state, move)

            newState['board'][playerIndex].append(move)

            for case in cases:
                newState['board'][otherIndex].remove(case)
                newState['board'][playerIndex].append(case)
            
        newState['current'] = otherIndex
        
        return newState

    return state, next



def coinparty(state):
    player = state["current"]
    player_2 = (player+1)%2
    currentP = len(state["board"][player])
    otherP = len(state["board"][player_2])
    return 100*((currentP-otherP)/(currentP+otherP))


def cornerCaptured(state):
    corners = [0, 7, 56, 63]
    player = state['current']
    player_2 = (player+1)%2
    currentP = state["board"][player]
    currentCorners = 0
    otherP = state["board"][player_2]
    otherCorners = 0
    for i in currentP:
        if i in corners:
            currentCorners += 1
    for i in otherP:
        if i in corners:
            otherCorners += 1
    try : 
        res = 100 * (currentCorners - otherCorners) / (currentCorners + otherCorners)
    except ZeroDivisionError:
        res = 0
    return res

def mobility(state):
    player = state['current']
    player_2 = (player+1)%2
    player_mob = len(possibleMoves(state))
    state_2 = copy.deepcopy(state)
    state_2['current'] = player_2
    player_2_mob = len(possibleMoves(state_2))
    try : 
        res = 100*((player_mob-player_2_mob)/(player_mob+player_2_mob))
    except ZeroDivisionError:
        res = 0
    return res

def stable(state):
    player = state['current']
    player_2 = (player+1)%2
    sides = [[i for i in range(1,7)], [i for i in range(8, 49) if i % 8 == 0], [i for i in range(57, 63)], [15,23,31,39,47,55]]
    player_stab = [i for i in state["board"][player] if i in sides]
    player_2_stab = [i for i in state["board"][player_2] if i in sides]
    try :
        res = 50*((len(player_stab)-len(player_2_stab))/(len(player_stab)+len(player_2_stab)))
    except ZeroDivisionError:
        res = 0
    return res
    

    
def heuristic(state, player= None):
    player = state['current']
    return coinparty(state) + cornerCaptured(state) + mobility(state) + stable(state)
    

def negamaxWithPruningIterativeDeepening(state, player, timeout=0.7):
    cache = defaultdict(lambda : 0)

    def cachedNegamaxWithPruningLimitedDepth(state, player, depth, alpha=float('-inf'), beta=float('inf')):
        over = isGameOver(state)
        if over or depth == 0:
            res = -heuristic(state, player), None, over
        else:
            theValue, theMove, theOver = float('-inf'), None, True
            possibilities = [(move, next(state, move)) for move in possibleMoves(state)]
            possibilities.sort(key=lambda poss: cache[tuple(poss[1])])
            for move, successor in reversed(possibilities):
                value, _, over = cachedNegamaxWithPruningLimitedDepth(successor, (player+1)%2, depth-1, -beta, -alpha)
                theOver = theOver and over
                if value > theValue and value != float("-inf") or value != float("inf"):
                    theValue, theMove = value, move
                    alpha = max(alpha, theValue)
                if alpha >= beta:
                    break
            res = -theValue, theMove, theOver
            cache[tuple(state)] = res[0]
        return res

    value, move = 0, None
    depth = 1
    start = time.time()
    over = False

    while value > -350 and time.time() - start < timeout and not over:
        value, move, over = cachedNegamaxWithPruningLimitedDepth(state, player, depth)
        depth += 1
    print("depth:", depth, "value:", value)
    return value, move

@timeit
def next_branch(state, fct):
    player = state['current']
    _, move = fct(state, player)
    return move

def random_choice(state):
    moves = possibleMoves(state)
    res = None
    if moves != []:
        res =  random.choice(moves)
    return res

Game = Othello
state, next = Game(['LB', 'LB'])
