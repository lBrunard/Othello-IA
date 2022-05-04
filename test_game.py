import pytest 
import serverPerso as sp
import jeu

request_server = {
   "request": "play",
   "lives": 3,
   "errors": [],
   "state": []
}

init_state = {
   "players": ["LUR", "LRG"],
   "current": 0,
   "board": [
      [28, 35],
      [27, 36]
   ]
}

def test_jeu():
    assert jeu.possibleMoves(init_state) == [19,26,37,44]
    assert jeu.willBeTaken(init_state, 19) == [27]
    assert jeu.isGameOver