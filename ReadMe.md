![Gitlab code coverage](https://img.shields.io/gitlab/coverage/lBrunard/Othello-IA/main_2?style=plastic)
![Testspace pass ratio](https://img.shields.io/testspace/pass-ratio/lBrunard/Othello-IA/main_2)

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




## License
Luis Brunard (20078)