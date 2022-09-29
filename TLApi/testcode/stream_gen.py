import time
from random import random


def stream_of_ints():
    for ent in range(200):
        yield ent
        time.sleep(random())

if __name__=='__main__':
    for en in stream_of_ints():
        print(f'{en}')
