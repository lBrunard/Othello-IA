import socket

def create_socket():
    with socket.socket() as s:
        s.bind(('localhost', 1234))
    