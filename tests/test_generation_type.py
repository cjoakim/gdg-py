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


    # assertions after .gdg state is established
    state = g.get_state()
    assert(len(state.keys()) == 4)
    assert(state['generations'] == 10)
    assert(state['pattern']     == 'sample-%.txt')
    assert(state['value_param'] == 'g')
    assert(state['regexp']      == 'sample-\\d\\d\\d\\d\\d\\d.txt')

    # assert initial set of files
    assert(g.previous() == None)
    assert(g.current() == None)
    assert(g.all_generations() == [])
    assert(g.all_files() == [])

    assert(g.next() == 'tmp/generations/sample-000001.txt')

    for i in range(1, 21):  # write files 000001 through 000020
        fname = g.next()
        __write(fname, 'this if file {}'.format(i))
    
    assert(g.previous() == 'tmp/generations/sample-000019.txt')
    assert(g.current()  == 'tmp/generations/sample-000020.txt')

    assert(len(g.all_generations()) == 10)
    assert(len(g.all_generations(limited=False)) == 20)
    assert(len(g.all_files()) == 20)

    assert(g.prune() == 10)
    assert(g.prune() == 0)

    assert(len(g.all_generations()) == 10)
    assert(len(g.all_generations(limited=False)) == 10)
    assert(len(g.all_files()) == 10)

    expected_files_list = [
        'tmp/generations/sample-000011.txt', 
        'tmp/generations/sample-000012.txt', 
        'tmp/generations/sample-000013.txt', 
        'tmp/generations/sample-000014.txt', 
        'tmp/generations/sample-000015.txt', 
        'tmp/generations/sample-000016.txt', 
        'tmp/generations/sample-000017.txt', 
        'tmp/generations/sample-000018.txt', 
        'tmp/generations/sample-000019.txt', 
        'tmp/generations/sample-000020.txt'
    ]

    assert(g.all_files() == expected_files_list)
    assert(g.all_generations() == expected_files_list)
    assert(g.all_generations(limited=False) == expected_files_list)

# private methods

def __test_directory():
    return 'tmp/generations'

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

