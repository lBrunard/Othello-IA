import pytest
import jeu
import serverPerso
import game
import socket

# class test_jeu:
#     def __init__(self):
#         self.state =  {
#             'players': ["Player 1", "Player 2"],
#             'current': 0,
#             'board': [
#                 [28,35],
#                 [27,36]
#             ]
#         }

state =  {
            'players': ["Player 1", "Player 2"],
            'current': 0,
            'board': [
                [28,35],
                [27,36]
            ]
        }
def test_jeu():
    assert jeu.possibleMoves(state=state) == [19, 26, 37, 44]
    assert jeu.willBeTaken(state, 19) == [27]
    assert jeu.isGameOver(state) == False
    state_2 = state
    state_2["board"][0] = []
    assert jeu.isGameOver(state_2) == True
    try :
        res = jeu.willBeTaken(state, -1)
    except game.BadMove:
        assert True
    state_2['board'][0] = [0]
    state_2['board'][1] = [7]
    assert jeu.heuristic(state) == 0
    assert jeu.random_choice(state) == None
    state_2 = state
    state_2["board"][0] = [28]
    state_2["board"][1] = [36]
    assert jeu.random_choice(state) == 44
    try :
        assert jeu.next(state, None) == state
    except game.BadMove:
        assert True
    
def test_jeu_2():
    state = {
            'players': ["Player 1", "Player 2"],
            'current': 0,
            'board': [  
                [28,35],
                [27,36]
            ]
        }
    assert jeu.next_branch(state, jeu.negamaxWithPruningIterativeDeepening) == 19

def test_game():
    try:
        jeu.willBeTaken(state, -1)
    except game.BadMove:
        assert True








