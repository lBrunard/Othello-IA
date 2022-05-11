from re import I
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
        assert False
    except game.BadMove:
        assert True
    



        


