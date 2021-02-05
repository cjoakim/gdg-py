import json
import sys
import time
import os

import arrow 

import gdg

if __name__ == "__main__":
    print('main')
    g = gdg.Gdg('data/date_based/.gdg')
    print(g)
    try:
        print('set_generations...')
        print(g.set_generations(10))
        print('set_pattern...')
        print(g.set_pattern('test---{}---{}---{}---{}.txt', ['e', 'ts_utc', 'ts_local', 'g']))
        print('next...')
        print(g.next())
    except:
        print(g)
