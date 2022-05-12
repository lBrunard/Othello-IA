import socket
import threading
import json
import jeu

inscription = json.dumps({
   "request": "subscribe",
   "port": 8888,
   "name": "Luis Brunard",
   "matricules": ["20078", "20078"]
})
# inscription_2 =json.dumps({
#    "request": "subscribe",
#    "port": 7777,
#    "name": "Client 2",
#    "matricules": ["CL2", "CL2"]
# })

move_resp = {
   "response": "move",
   "move": "the_move_played",
   "message": "El paquito"
}

ping_message = json.dumps({"request": "ping"})
pong_message = json.dumps({"response": "pong"})

def subscribe():
    sender_address = ("127.0.0.1", 3000)
    with socket.socket() as s:
        s.connect(sender_address)
        s.send(inscription.encode())
        s.close()
    # with socket.socket() as s:
    #     s.connect(sender_address)
    #     s.send(inscription_2.encode())
    #     s.close()
    
def sender(message, client):
    client.send(message.encode())

def reciev_1():
    rc_address = ("127.0.0.1", 8888)
    with socket.socket() as so:
        try:
            so.bind(rc_address)
        except OSError:
            print("Port already in use")
            reciev_1()
        so.listen()
        while True:
            client, address = so.accept()
            with client:
                message = client.recv(2048).decode()
                checker(message, client, "Client 1")
                client.close()

# def reciev_2():
#     rc_address = ("127.0.0.1", 7777)
#     with socket.socket() as so:
#         try:
#             so.bind(rc_address)
#         except OSError:
#             print("Port already in use")
#             reciev_2()
#         so.listen()
#         while True:
#             client, address = so.accept()
#             with client:
#                 message = client.recv(2048).decode()
#                 checker(message, client, "Client 2")
#                 client.close()

def play_1(message, client, player):
    state = message["state"]
    final = move_resp
    res = jeu.next_branch(state, jeu.negamaxWithPruningIterativeDeepening)
    if res == None:
        final["move"] = None
        return sender(json.dumps(final), client)
    final["move"] = res
    return sender(json.dumps(final), client)
 
    

# def play_2(message, client, player):
#     state = message["state"]
#     final = move_resp
#     res = jeu.random_choice(state)
#     if res == None:
#         final["move"] = None
#         return sender(json.dumps(final), client)
#     final["move"] = res
#     return sender(json.dumps(final), client)
    

def checker(message, client, player):
    m = json.loads(message)
    if message == ping_message:
        sender(pong_message, client)
        print("connected")
    if m["request"] == "play" and player == "Client 1":
        play_1(m, client, player)
    # if m["request"] == "play" and player == "Client 2":
    #     play_2(m, client, player)


if "__main__" == __name__:
    subscribe()
    thread1 = threading.Thread(target=reciev_1, daemon=True)
    thread1.start()
    # reciev_2()