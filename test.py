import time
import threading
from typing import Counter

def t():
    counter = 0 
    while True:
        counter += 1

    return counter

if __name__ == '__main__':
    t = threading.Thread(target=t).start()
    r = t.get(counter)
    print(r)

        