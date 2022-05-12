import threading
import time

def printer():
    while True:
        print("Hello")
        time.sleep(1)





if "__main__" == __name__:
    thread = threading.Thread(target=printer)
    thread.join(5)
    