import socket
import threading
import json
import jeu
import random
import time
import sys

inscription = json.dumps({
   "request": "subscribe",
   "port": "0",
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

class client:
    def __init__(self, name, port, type, host):
        self.name = name
        self.port = port
        self.type = type
        self.sender_addr = (host, 3000)

    def __str__(self):
        if self.thread.is_alive():
            return "Client " + self.name + " is alive"
        return "Client" + self.name + " is dead"
    
    def __del__(self):
        self.client.close()
        self.join_tread()

    def subscribe(self):
        print("Creating Client")
        inscription = json.dumps({
            "request": "subscribe",
            "port": self.port,
            "name": self.name,
            "matricules": [self.type, str(self.port)]
        })
        with socket.socket() as s:
            s.connect(self.sender_addr)
            s.send(inscription.encode())
            s.close()
        self.create_thread()
        
    def create_thread(self):
        self.thread = threading.Thread(target=self.reciev)
        self.thread.daemon = True
        self.thread.start()

    def join_tread(self):
        self.thread.join()


    def reciev(self):
        print("Listening on port " + str(self.port))
        rc_address = ("localhost", self.port)
        with socket.socket() as so:
            so.bind(rc_address)
            so.listen()
            while True:
                print("Waiting for connection")
                self.client, address = so.accept()
                with self.client:
                    print("Client " + self.name + " connected")
                    message = self.client.recv(2048).decode()
                    print(message)
                    if message == ping_message:
                        self.ping()
                    self.play(json.loads(message))
                    self.client.close()
                    print("Client " + self.name + " disconnected")


    def sender(self, message):
        self.client.send(message.encode())

    def ping(self):
        self.sender(pong_message)
    
    def play(self, message):
        state = message["state"]
        send = move_resp
        if self.type == "random":
            res = jeu.random_choice(state)
        elif self.type == "negamax":
            res = jeu.next_branch(state, jeu.negamaxWithPruningIterativeDeepening)
        if res == None:
            send["move"] = None
            return self.sender(json.dumps(send))
        send["move"] = res
        return self.sender(json.dumps(send))

if "__main__" == __name__:
    ports = [i for i in range(3000, 5000)]
    clients = []
    client_1 = client("Client 1", random.choice(ports), "random", "localhost")
    client_1.subscribe()
    #client_1.create_thread()
    clients.append(client_1)
    time.sleep(1)
    client_2 = client("Client 2", random.choice(ports), "negamax", "localhost")
    client_2.subscribe()
    #client_2.create_thread()
    clients.append(client_2)
    try:
        while True:
            time.sleep(1)
            print(client_1)
            print(client_2)
    except KeyboardInterrupt:
        for i in clients:
            del i
        print("Exiting")
        sys.exit()
    


