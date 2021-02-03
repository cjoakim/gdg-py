import json
import sys
import time
import os

import arrow 

import gdg

if __name__ == "__main__":
    print('main')
    g = gdg.Gdg('data')
    print(g)
    g.set_count(10)
