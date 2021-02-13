gdg - generation data groups with python
========================================

Features
--------

- Acts similarly to an IBM Mainframe GDG - Generation Data Group 
- You define the number of generations, or versions, in the gdg 
- The Gdg specifies a filesystem directory, a filename pattern, and a number of generations to keep
- Invoke method next() to get the next logical filename 
- Invoke method current() to get the current, or most recent, filename
  Invoke method previous() to get the filename before current()
- Invoke method all_generations() to get all filenames within the gdg
- Invoke method prune() to delete the older files greater than the number of generations 

Why Use this Library?
---------------------------
- To keep your filenames tidy
- To keep your directories tidy, delete older/obsolete generations 
- You come from a "big iron" background and miss the concept of a GDG on linux/mac/windows
- You like regular expressions

The Four Patterns supported, and Examples:
------------------------------------------

.. code-block:: console

    Filename                       Gdg Type 

    sample-000020.txt              Generation number type, 'g'
    sample-1612735756.txt          Epoch type, 'e'
    sample-20210207-172005.txt     UTC Timestamp type, 'ts_utc'
    sample-20210207-172005.txt     Local Timestamp type, 'ts_local'

Quick start
-----------

Installation:

.. code-block:: console

    $ pip install gdg

Use:

Case 1: filenames with an embedded generation number ('g') sequence

.. code-block:: pycon

    >>> import gdg

    >>> g = gdg.Gdg(...some_dir_path...)
    >>> g.set_pattern('sample-%.txt', 'g')  # 'g' for incrementing generation number
    >>> g.set_generations(3)                # set the number of generations to any positive int 

    >>> n = g.get_generations()  # returns the int number of generations to retain in the gdg 
    >>> jstr = g.get_state()     # returns the state of the gdg as a dict

    >>> filename = g.next()  # obtain the next filenamed in the gdg, YOUR code writes to the file 
    >>> filename = g.next()
    >>> filename = g.next()

    >>> fname = g.current()          # returns a string filename or None
    >>> fname = g.previous()         # returns a string filename or None
    >>> flist = g.all_generations()  # returns a list
    >>> flist = g.all_files()        # returns a list 
    >>> flist = g.all_files()

    >>> n = g.prune()  # returns the number of files deleted, retains the most recent g.get_generations() number of files

Case 2: filenames with an embedded epoch ('e') time

.. code-block:: pycon

    >>> import gdg

    >>> g = gdg.Gdg(...some_dir_path...)
    >>> g.set_generations(24)
    >>> g.set_pattern('sample-%.txt', 'e')  # 'e' for epoch time

    >>> # same usage otherwise as in Case 1 above

Case 3: filenames with an embedded UTC Timestamp ('ts_utc') time

.. code-block:: pycon

    >>> import gdg

    >>> g = gdg.Gdg(...some_dir_path...)
    >>> g.set_pattern('sample-%.txt', 'ts_utc')  # 'ts_utc' for UTC Timestamp
    >>> g.set_generations(24)

    >>> # same usage otherwise as in Case 1 above

Case 4: filenames with an embedded Local Timestamp ('ts_utc') time

.. code-block:: pycon

    >>> import gdg

    >>> g = gdg.Gdg(...some_dir_path...)
    >>> g.set_pattern('sample-%.txt', 'ts_local')  # 'ts_local' for Local Timestamp
    >>> g.set_generations(40)

    >>> # same usage otherwise as in Case 1 above


Source Code
===========

See https://github.com/cjoakim/gdg-py

Changelog
=========

Version 0.1.0
-------------

-  2021/02/13. 0.1.0 Beta
-  2021/02/07. 0.0.2 Pre-Alpha
-  2021/02/02. 0.0.1 Pre-Alpha
-  2021/02/02. 0.0.0 Pre-Alpha
