import socket
import threading
import json
import importlib
import random
import sys
import copy
import game


gameName = 'othello'



inscription = json.dumps({
   "request": "subscribe",
   "port": 8888,
   "name": "Client 1",
   "matricules": ["CL1", "CL1"]
})
inscription_2 =json.dumps({
   "request": "subscribe",
   "port": 7777,
   "name": "Client 2",
   "matricules": ["CL2", "CL2"]
})

move_resp = {
   "response": "move",
   "move": "the_move_played",
   "message": "Fun message"
}

ping_message = json.dumps({"request": "ping"})
pong_message = json.dumps({"response": "pong"})

def subscribe():
    sender_address = ("127.0.0.1", 3000)
    with socket.socket() as s:
        s.connect(sender_address)
        s.send(inscription.encode())
        s.close()
    with socket.socket() as s:
        s.connect(sender_address)
        s.send(inscription_2.encode())
        s.close()
    

def sender(message, client):
    client.send(message.encode())

def reciev_1():
    rc_address = ("127.0.0.1", 8888)
    with socket.socket() as so:
        so.bind(rc_address)
        so.listen()
        while True:
            client, address = so.accept()
            with client:
                message = client.recv(2048).decode()
                player = client.getsockname()[1]
                checker(message, client, "Client 1")
                client.close()

def reciev_2():
    rc_address = ("127.0.0.1", 7777)
    with socket.socket() as so:
        so.bind(rc_address)
        so.listen()
        while True:
            client, address = so.accept()
            with client:
                message = client.recv(2048).decode()
                player = client.getsockname()[1]
                checker(message, client, "Client 2")
                client.close()


def play(message, client, player): 
    state = message["state"]
    moves = game.possibleMoves(state)
    print("Possible moves:",moves)
    if len(moves) < 1:
        return sender(json.dumps({"response" : "giveup",}), client)
    last_dif = 0
    best_array = []
    play = 0
    other = 1
    if player == "Client 2" and state["current"] == 1:
        play = 1
        other = 0
    for move in moves:
        next_board = game.next(state, move)
        dif = len(next_board["board"][play]) - len(next_board["board"][other])
        print("\nMove:", move)
        print("DIF :", dif)
        if dif > 0 and dif > last_dif:
            print("Give", len(next_board["board"][play]), "vs", len(next_board["board"][other]))
            print("GOOD MOVE")
            best_array.append(move)
            last_dif = dif
        elif dif == last_dif:
            best_array.append(move)
    if last_dif == 0:
        best_array.append(random.choice(moves))
        print("RANDOM MOVE", best_array)
    final = move_resp
    final["move"] = random.choice(best_array)
    return sender(json.dumps(final), client)

def checker(message, client, player):

    m = json.loads(message)
    if message == ping_message:
        sender(pong_message, client)
    if m["request"] == "play":
        play(m, client, player)


subscribe()
thread = threading.Thread(target=reciev_1, daemon=True)
thread.start()
reciev_2()