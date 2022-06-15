import socket
import time

def create_socket():
    while True:
        time.sleep(0.5)
        with socket.socket() as s:
            s.connect(("localhost", 10000))
            s.send("Hello World")
            s.close()

create_socket()
    