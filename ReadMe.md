# Othello IA project

IA created for the purpose of the PI2C course project.

## Start and connection

To connect you must launch the file serverPerso.py and the AI automatically connects to the game server


## Strategies 
Strategies are calculated by heuristic functions
### Coin Party

```py
def coinparty(state):
    player = currentPlayer(state)
    player_2 = otherplayer(player)
    currentP = len(state["board"][player])
    otherP = len(state["board"][player_2])
    return 100*((currentP-otherP)/(currentP+otherP))
```
This function calculates the number of pawns that each player will have at the next move. It returns a value between -100 and 100. -100, the opposing player has all the pawns and vice versa

### Corner Captured
```py
def cornerCaptured(state):
    corners = [0, 7, 56, 63]
    player = currentPlayer(state)
    player_2 = otherplayer(player)
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
```
Since when a corner is taken, it cannot be taken back. Taking a corner gives more weight to the shot.
If there are no corners taken, the function returns a value of 0.
Like coinParty, the function normally returns a value between -100 and 100
### Mobility
```py
def mobility(state):
    player = state['current']
    player_2 = (player+1)%2
    player_mob = len(possibleMoves(state))
    state_2 = copy.deepcopy(state)
    state_2['current'] = player_2
    player_2_mob = len(possibleMoves(state_2))
    print(player_mob, player_2_mob)
    try : 
        res = 100*((player_mob-player_2_mob)/(player_mob+player_2_mob))
    except ZeroDivisionError:
        res = 0
    return res
```
The mobility function calculates the number of moves it will be possible to play for each of the 2 players. En returns a value between -100 and 100 like the other heuristic functions

### Stability
```py
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
```
The stable function calculates the number of sides that each player will have at the traded move. The function returns a value between 50 and -50, the half of the function concerning the corners because the corners cannot be taken and the sides are more likely to be taken

## License
Luis Brunard (20078)