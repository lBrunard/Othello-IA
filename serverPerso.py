import socket
import threading
import json
import jeu
import random
import sys

inscription = json.dumps({
   "request": "subscribe",
   "port": 0,
   "name": "Client 1",
   "matricules": ["20078", "20070"]
})

move_resp = {
   "response": "move",
   "move": "the_move_played",
   "message": "El paquito"
}

ping_message = json.dumps({"request": "ping"})
pong_message = json.dumps({"response": "pong"})

def creat_listener(port, name, type):
    name = threading.Thread(target=reciev, args=(port,name, type))
    name.start()

def subscribe():
    types = ["random", "negamax"]
    for i in range(int(sys.argv[2])):
        port = random.randint(10000, 60000)
        type = random.choice(types)
        sender_address = (sys.argv[1], 3000)
        with socket.socket() as s:
            s.connect(sender_address)
            inscription["port"] = str(port)
            s.send(inscription.encode())
            s.close()
        creat_listener(port, "Client {}, {}".format(i+1, type), type)

def sender(message, client):
    client.send(message.encode())

def reciev(port, name, type):
    rc_address = ("localhost", port)
    with socket.socket() as so:
        so.bind(rc_address)
        so.listen()
        while True:
            client, address = so.accept()
            with client:
                message = client.recv(2048).decode()
                checker(message, client, name, type)
                client.close()


def play_negamax(message, client, player):
    state = message["state"]
    final = move_resp
    res = jeu.next_branch(state, jeu.negamaxWithPruningIterativeDeepening)
    if res == None:
        final["move"] = None
        return sender(json.dumps(final), client)
    final["move"] = res
    return sender(json.dumps(final), client)

def play_random(message, client, player):
    state = message["state"]
    final = move_resp
    res = jeu.random_choice(state)
    if res == None:
        final["move"] = None
        return sender(json.dumps(final), client)
    final["move"] = res
    return sender(json.dumps(final), client)

  

def checker(message, client, player):
    m = json.loads(message)
    if message == ping_message:
        sender(pong_message, client)
        print("connected")
    if m["request"] == "play" and type == "random":
        play_random(m, client, player)
    if m["request"] == "play" and type == "negamax":
        play_negamax(m, client, player)


if "__main__" == __name__:
    subscribe()
