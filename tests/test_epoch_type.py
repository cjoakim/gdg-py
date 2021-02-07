import pytest

import glob
import os

import gdg


def test_epoch_type_gdg():
    directory = __prune_test_directory()

    g = gdg.Gdg(directory)
    g.set_generations(20)
    g.set_pattern('sample-%.txt', 'e')

    state = g.get_state()
    assert(len(state.keys())    == 4)
    assert(state['generations'] == 20)
    assert(state['pattern']     == 'sample-%.txt')
    assert(state['value_param'] == 'e')
    assert(state['regexp']      == 'sample-\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d.txt')



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


