from re import I
import socket
import threading
import json
import jeu
import random




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
                checker(message, client, "Client 2")
                client.close()


def play_2(message, client, player):
    state = message["state"]
    final = move_resp
    res = jeu.next_branch(state, jeu.negamaxWithPruningLimitedDepth)
    print(res)
    if res == None:
        final["move"] = None
        return sender(json.dumps(final), client)
    final["move"] = res
    return sender(json.dumps(final), client)


def play(message, client, player): 
    state = message["state"]
    final = move_resp
    res = jeu.best_move(state)
    if res == None:
        final["move"] = res
        return sender(json.dumps(final), client)
    else:
        final = move_resp
        final["move"] = res
        return sender(json.dumps(final), client)


def checker(message, client, player):

    m = json.loads(message)
    if message == ping_message:
        sender(pong_message, client)
        print("connected")
    elif m["request"] == "play" and player == "Client 1":
        #print(m["errors"])
        play_2(m, client, player)
    elif m["request"] == "play" and player == "Client 2":
        play(m, client, player)
    


subscribe()
thread1 = threading.Thread(target=reciev_1, daemon=True)
# thread2 = threading.Thread(target=reciev_3, daemon=True)
# thread3 = threading.Thread(target=reciev_4, daemon=True)
thread1.start()
# thread2.start()
# thread3.start()
reciev_2()