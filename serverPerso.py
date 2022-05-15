import socket
import threading
import json
import jeu
import sys

inscription = json.dumps({
   "request": "subscribe",
   "port": 4440,
   "name": "El paquito",
   "matricules": ["20078", "12345"]
})

move_resp = {
   "response": "move",
   "move": "the_move_played",
   "message": "El paquito"
}

ping_message = json.dumps({"request": "ping"})
pong_message = json.dumps({"response": "pong"})

def subscribe():
    sender_address = (sys.argv[1], port)
    with socket.socket() as s:
        s.connect(sender_address)
        s.send(inscription.encode())
        s.close()
    
def sender(message, client):
    client.send(message.encode())

def reciev_1():
    rc_address = ("localhost", 4440)
    with socket.socket() as so:
        so.bind(rc_address)
        so.listen()
        while True:
            client, address = so.accept()
            with client:
                message = client.recv(2048).decode()
                checker(message, client, "El paquito")
                client.close()

def play_1(message, client, player):
    state = message["state"]
    final = move_resp
    res = jeu.next_branch(state, jeu.negamaxWithPruningIterativeDeepening)
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
    if m["request"] == "play" and player == "El paquito":
        play_1(m, client, player)


if "__main__" == __name__:
    try:
        if sys.argv[2]:
            port = int(sys.argv[2])
    except IndexError:
        port = 3000
    print(port)
    print(type(port))
    subscribe()
    thread_rc_1 = threading.Thread(target=reciev_1).start()