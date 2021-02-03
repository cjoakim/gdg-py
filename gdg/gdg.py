__author__ = 'cjoakim'

import json
import sys
import time
import os


class Gdg(object):
    """

    """
    def __init__(self, path):
        self.path = path
        print('init; path: {}'.format(path))

    def set_count(self, n):
        self.count = int(n)
        print('set_count: {}'.format(self.count))

    def __str__(self):
        return "<Gdg path:{0}>".format(self.path)
