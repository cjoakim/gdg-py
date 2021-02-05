__author__ = 'cjoakim'

import json
import os
import re
import sys
import time
import traceback

from datetime import datetime, date, timezone

FORMAT_GENERATION = 'g'
FORMAT_EPOCH      = 'e'
FORMAT_TIMESTAMP_UTC = 'ts_utc'
FORMAT_TIMESTAMP_LOCAL = 'ts_local'
VALID_FORMATS = [
    FORMAT_GENERATION,
    FORMAT_EPOCH,
    FORMAT_TIMESTAMP_UTC,
    FORMAT_TIMESTAMP_LOCAL
]

FORMAT_TIMESTAMP = '%Y-%m-%d-%H:%M:%S'

RE_GENERATION = '\d\d\d\d\d\d'  # 6 digits
RE_EPOCH      = '\d\d\d\d\d\d\d\d\d\d'  # 1612529215 (10 digits)
RE_TIMESTAMP  = '\d\d\d\d-\d\d-\d\d-\d\d:\d\d:\d\d'  # 2021-02-05-07:56:23


class Gdg(object):
    """

    """
    def __init__(self, path='.gdg', verbose=False):
        self.path = path
        self.state = self.__read_state()
        self.verbose = verbose
        if self.verbose:
            print('init; path: {} state: {}'.format(self.path, self.state))

    def set_generations(self, n):
        if int(n) > 0:
            self.state['generations'] = int(n)
            self.__write_state()

    def set_max_days(self, n):
        if int(n) > 0:
            self.state['max_days'] = int(n)
            self.__write_state()

    def set_pattern(self, pattern, param_list):
        try:
            curr_state = self.__read_state()  # capture current state in case of restore
            self.state['pattern'] = pattern.strip()
            self.state['param_list'] = self.__parse_parm_list(param_list)
            self.state['regexp'] = self.__set_regexp()
            s = self.next()  # will throw an exception if pattern is invalid, discard s
            return True
        except Exception as e:
            self.state = curr_state  # restore the state from before this method invocation
            traceback.print_exc()
            raise e

    def set_verbose(self, bool=True):
        if bool == True:
            self.verbose = True
        if bool == False:
            self.verbose = False

    def next(self):
        #return 'first: {} second:{}'.format(*['a', 'b'])
        template = self.state['pattern']
        values = list()
        for p in self.state['param_list']:
            if p == FORMAT_GENERATION:
                n = 1 # todo, read fs to get current n
                values.append('{0:06d}'.format(n))
            if p == FORMAT_EPOCH:
                values.append(int(time.time()))
            if p == FORMAT_TIMESTAMP_UTC:
                values.append(datetime.utcnow().strftime(FORMAT_TIMESTAMP))
            if p == FORMAT_TIMESTAMP_LOCAL:
                values.append(datetime.now().strftime(FORMAT_TIMESTAMP))
        return template.format(*values)

    def current(self):
        pass

    def previous(self):
        pass

    def all(self):
        pass

    def prune(do_deletes=False):
        # return a list of filenames, optionally delete them
        pass

    # dunder methods

    def __str__(self):
        return "<Gdg path:{} state:{}>".format(self.path, json.dumps(self.state))
        
    # private methods follow 

    def __parse_parm_list(self, param_list):
        parsed_param_list = list()
        try:
            for p in param_list:
                if p.lower() in VALID_FORMATS:
                    parsed_param_list.append(p.lower())
                else:
                    raise Exception('Invalid filename pattern parameters list: {}'.format(param_list))
        except:
            raise Exception('Invalid filename pattern parameters list: {}'.format(param_list))
        return parsed_param_list

    def __set_regexp(self):
        # self.state['pattern'] = pattern.strip()
        # self.state['param_list']

        # TODO - handle case where pattern starts and/or ends with {}?
        pattern_tokens = self.state['pattern'].split('{}')   
        regexp_tokens = list()
        for token in pattern_tokens:
            pass

            # RE_GENERATION = '\d\d\d\d\d\d'  # 6 digits
            # RE_EPOCH      = '\d\d\d\d\d\d\d\d\d\d'  # 1612529215 (10 digits)
            # RE_TIMESTAMP  = '\d\d\d\d-\d\d-\d\d-\d\d:\d\d:\d\d'  # 2021-02-05-07:56:23

        return 'todo'
        
    def __read_state(self):
        try:
            with open(self.path, 'rt') as f:
                return json.loads(f.read())
        except:
            return {}

    def __write_state(self):
        with open(self.path, 'w') as f:
            jstr = json.dumps(self.state)
            f.write(jstr)
            if self.verbose:
                print('state:{}'.format(jstr))


# g = Gdg(dir, name='.gdg')   # the spec file defaults to .gdg, but others can be created
# g.set_generations(n)           # updates the .gdg file
# g.set_max_days(n)           # updates the .gdg file
# g.set_pattern(s, params)    # sets the filename pattern and parameters

# fn = g.current()
# fn = g.previous()
# fn_list = g.all()
# fn = g.next()
# fn_list = g.prune_list(do_deletes=False, retain_count=-1)



