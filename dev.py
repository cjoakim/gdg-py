import json
import sys
import time
import os
import traceback

import arrow 

import gdg

if __name__ == "__main__":
    print('main')
    g = gdg.Gdg('tmp/generations', True)

    try:
        print('set_generations...')
        print(g.set_generations(10))
        print('set_pattern...')
        print(g.set_pattern('sample-%.txt', 'g'))
  
        print('next...')
        print(g.next())

        print('all_files...')
        print(g.all_files())
        print(len(g.all_files()))

        print('all_generations...')
        print(g.all_generations())
        print(len(g.all_generations()))

        print('current...')
        print(g.current())

        print('previous...')
        print(g.previous())

        print('get_state...')
        print(g.get_state())

        print('next...')
        print(g.next())

        print('prune...')
        g.prune()

    except Exception as e:
        traceback.print_exc()
