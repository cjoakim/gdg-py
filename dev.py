import json
import sys
import time
import os
import traceback

import arrow 

import gdg

if __name__ == "__main__":
    print('main')
    g = gdg.Gdg('data/gen_based', True)

    try:
        print('set_generations...')
        print(g.set_generations(10))
        print('set_pattern...')
        print(g.set_pattern('sample-%.txt', 'g'))
  
        print('next...')
        print(g.next())

        files_list = g.all()
        for f in files_list:
            print('all: {}'.format(f))

        print('current...')
        print(g.current())

        print('previous...')
        print(g.previous())

        print('get_state...')
        print(g.get_state())

        print('next...')
        print(g.next())

    except Exception as e:
        traceback.print_exc()
