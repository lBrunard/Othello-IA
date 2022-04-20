import random
import time
M_Dir = [(-1, -1), (-1, 0), (-1, +1),
        (0, -1),           (0, +1),
        (+1, -1), (+1, 0), (+1, +1)]

class board:
    def __init__(self, n):
        self.player = 1
        number = 0
        self.n = n
        self.board = []
        self.num_board = []
        for i in range(self.n):
            self.board.append([])
            self.num_board.append([])
            for j in range(self.n):
                self.board[i].append(0)
                self.num_board[i].append(number)
                number += 1
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1

    def __str__(self):
        final = ""
        final += "     0   1   2   3   4   5   6   7\n"
        final += "   +---+---+---+---+---+---+---+---+\n"
        c = 0
        for i in range(self.n):
            l = f"{i} | "
            for j in range(self.n):
                c = self.board[i][j]
                if c == 0:
                    l+= "   "
                elif c == 1:
                    l += " * "
                else:
                    l+=" 0 "
                l+= "|"
            final += f"{l}\n"
            final += "   +---+---+---+---+---+---+---+---+\n"
        return final

    def update(self, x, y, value = 0):
        self.board[x][y] = value

    def is_tile(self,x,y):
        if self.board[x][y] == 0:
            return True
        return False

    def coords_on_plate(self, x, y):
        if 0<=x<self.n and 0<=y<self.n:
            return True
        return False

    def valid_move(self, x = None, y = None, player=None):
        list_Pos_move = []
        it1 = 0
        for i in self.board:
            it2 = 0
            for j in i:
                for k, l in M_Dir:
                    x, y = it1 + k, it2 + l
                    if self.coords_on_plate(x,y) and self.board[it1][it2] == player:
                        pos = self.board[x][y]
                        if pos != player and pos  != 0 :
                            print(f"Possible move : {it1}:{it2} to {x}:{y}")
                            list_Pos_move.append([(it1,it2), (x,y)])
                it2 += 1
            it1 += 1
        return list_Pos_move
    def valid_prec_move(self, x, y, player):
        posib = []
        for i,j in M_Dir:
            pos = self.board[x + i][y + j]
            if pos != 0 and pos != player:
                posib.append((x+i,y+j))
        return posib

    def verif(self, x_b, y_b, x_a, y_a, player):
        init = self.board[x_b][y_b]
        mid = self.board[x_a][y_a]
        fin = 0
        posib = self.valid_prec_move(x_b, y_b,player)
        if init == player and mid!=0 and mid!= player  and (x_a, y_a) in posib:
            return True
        return False

    def next_tile(self, x_b, y_b, x_a, y_a):
        if x_b == x_a and y_b == y_a -1:
            print("Gauche")
            return (x_a, y_a+1)
        if x_b == x_a and y_b == y_a +1:
            print("Droite")
            return (x_a, y_a-1)
        if y_b == y_a and x_b == x_a -1:
            print("Bas")
            return (x_a+1, y_a)
        if y_b == y_a and x_b == x_a +1:
            print("Haut")
            return (x_a-1, y_a)
        if x_b == x_a +1 and y_b == y_a -1:
            print("Haut Gauche")
            return (x_a-1, y_a+1)
        if x_b == x_a +1 and y_b == y_a +1:
            print("Haut Droite")
            return (x_a-1, y_a-1)
        if x_b == x_a -1 and y_b == y_a -1:
            print("Bas Gauche")
            return (x_a+1, y_a+1)
        if x_b == x_a -1 and y_b == y_a +1:
            print("Bas Droite")
            return (x_a+1, y_a-1)
        raise Exception("ERREUR")

        
        
        

            
            
                    

        

b = board(8)


def play(player):
    m = random.choice(b.valid_move(player=1))
    x, y = b.next_tile(m[0][0], m[0][1], m[1][0], m[1][1])
    num = b.num_board[x][y]
    b.update(m[1][0], m[1][1], player)
    b.update(x, y, player)
    return num

def pVp():
    player = -1
    while True:
        if player == 1:
            player = -1
        else : player = 1
        print("Player : ", player)
        l = b.valid_move(player=player)
        x_b = int(input("X : "))
        y_b = int(input("Y : "))
        x_a = int(input("X : "))
        y_a = int(input("Y : "))
        if b.verif(x_b,y_b,x_a,y_a, player):
            next_tile = b.next_tile(x_b, y_b, x_a, y_a)
            print(next_tile)
            b.update(x_a, y_a, player)
            b.update(next_tile[0], next_tile[1], player)
        else:
            print("Not possible move")
        print(b)

def rVr():
    player = 1
    while True:
        if player == 1:
            player = -1
        else : player = 1
        print("Player : ", player)
        l = b.valid_move(player=player)
        m = random.choice(l)
        print(m)
        next_tile = b.next_tile(m[0][0], m[0][1], m[1][0], m[1][1])
        b.update(m[1][0], m[1][1], player)
        b.update(next_tile[0], next_tile[1], player)
        time.sleep(1)
        print(b)

#rVr()



## Check coords