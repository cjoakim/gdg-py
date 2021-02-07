import pytest

import glob
import os

import gdg


def test_generation_number_type_gdg():
    directory = __prune_test_directory()

    g = gdg.Gdg(directory)
    assert(g.get_state() == {})

    bool = g.set_generations(-1)
    assert(bool == False)

    bool = g.set_generations('ten')
    assert(bool == False)
    assert(g.get_state() == {})

    bool = g.set_generations('9')
    assert(bool == True)
    assert(g.get_state() == {'generations': 9})

    bool = g.set_generations(10)
    assert(g.get_state() == {'generations': 10})

    bool = g.set_pattern('sample-%.txt', 'Q')
    assert(bool == False)

    bool = g.set_pattern('sample-%.txt', 'g')
    assert(bool == True)

    state = g.get_state()

    assert(len(state.keys()) == 4)
    assert(state['generations'] == 10)
    assert(state['pattern']     == 'sample-%.txt')
    assert(state['value_param'] == 'g')
    assert(state['regexp']      == 'sample-\\d\\d\\d\\d\\d\\d.txt')



# private methods

def __test_directory():
    return 'tmp/epoch'

def __prune_test_directory():
    for f in glob.glob('{}/.gdg'.format(__test_directory())):
        os.remove(f)
    for f in glob.glob('{}/*'.format(__test_directory())):
        os.remove(f)
    return __test_directory()

def __write(outfile, s, verbose=True):
    with open(outfile, 'w') as f:
        f.write(s)
        if verbose:
            print('file written: {}'.format(outfile))
