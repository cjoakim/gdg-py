__author__ = 'cjoakim'

import json
import os
import re
import sys
import time
import traceback

from datetime import datetime, date, timezone
from inspect import currentframe, getframeinfo

from .constants import Constants


FORMAT_GENERATION = Constants.format_generation()
FORMAT_EPOCH      = Constants.format_epoch()
FORMAT_TIMESTAMP_UTC = 'ts_utc'
FORMAT_TIMESTAMP_LOCAL = 'ts_local'
VALID_FORMATS = [
    FORMAT_GENERATION,
    FORMAT_EPOCH,
    FORMAT_TIMESTAMP_UTC,
    FORMAT_TIMESTAMP_LOCAL
]

TIMESTAMP_FORMAT = '%Y-%m-%d-%H:%M:%S'

PARAMETER_CHAR = '%'

RE_TOKEN_MAP = dict()
RE_TOKEN_MAP[FORMAT_GENERATION] = '\\d\\d\\d\\d\\d\\d'  # 6 digits
RE_TOKEN_MAP[FORMAT_EPOCH]      = '\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d'  # 10 digits
RE_TOKEN_MAP[FORMAT_TIMESTAMP_UTC]   = '\\d\\d\\d\\d-\\d\\d-\\d\\d-\\d\\d:\\d\\d:\\d\\d'  # 2021-02-05-07:56:23
RE_TOKEN_MAP[FORMAT_TIMESTAMP_LOCAL] = '\\d\\d\\d\\d-\\d\\d-\\d\\d-\\d\\d:\\d\\d:\\d\\d'  # 2021-02-05-07:56:23

RE_GENERATIION_NUMBER = '\\d\\d\\d\\d\\d\\d'


class Gdg(object):
    """

    """
    def __init__(self, directory, verbose=False):
        self.directory = directory.strip()
        if self.directory.endswith(os.path.sep):
            self.directory = self.directory[:-1]
        self.verbose = verbose
        self.metafile = '{}{}.gdg'.format(self.directory, os.path.sep)
        self.state = self.__read_state()
        self.__write_state()

        if self.verbose:
            print('init, directory: {}'.format(self.directory))
            print('init, metafile:  {}'.format(self.metafile))
            print(str(self))

    def get_state(self):
        return self.__read_state()

    def set_generations(self, n):
        if int(n) > 0:
            self.state['generations'] = int(n)
            self.__write_state()

    def set_max_days(self, n):
        if int(n) > 0:
            self.state['max_days'] = int(n)
            self.__write_state()

    def set_pattern(self, pattern, value_param):
        try:
            curr_state = self.__read_state()  # capture current state in case of restore
            self.state['pattern'] = pattern.strip()
            self.state['value_param'] = self.__parse_value_param(value_param)
            self.state['regexp'] = self.__format_regexp()
            print('set_pattern before next()')
            s = self.next()  # will throw an exception if pattern is invalid, discard s
            print('set_pattern after next()')
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
        template = self.state['pattern'].replace('%', '{}')
        values = list()
        p = self.state['value_param']

        if p == FORMAT_GENERATION:
            f, n = self.current(), 1
            if f != None:
                n = self.__parse_generation_number(f)
                if n > 0:
                    n = n + 1
                else:
                    n = 1
            values.append('{0:06d}'.format(n))

        elif p == FORMAT_EPOCH:
            values.append(int(time.time()))

        elif p == FORMAT_TIMESTAMP_UTC:
            values.append(datetime.utcnow().strftime(TIMESTAMP_FORMAT))

        elif p == FORMAT_TIMESTAMP_LOCAL:
            values.append(datetime.now().strftime(TIMESTAMP_FORMAT))

        basename = template.format(*values)
        return '{}{}{}'.format(self.directory, os.path.sep, basename)

    def current(self):
        all = self.all_generations()
        if len(all) > 0:
            return all[-1]
        else:
            return None

    def previous(self):
        all = self.all_generations()
        if len(all) > 1:
            return all[-2]
        else:
            return None

    def all_generations(self):
        files_list, matched_list = self.__walk_fs(), list()
        compiled_re = re.compile('{}{}{}'.format(
            self.directory, os.path.sep, self.state['regexp']))
        for f in files_list:
            m = compiled_re.match(f)
            if m != None:
                matched_list.append(f)
        return sorted(matched_list)

    def all_files(self):
        return self.__walk_fs()

    def prune(do_deletes=False):
        # TODO return a list of filenames, optionally delete them 
        pass

    # dunder methods

    def __str__(self):
        return "<Gdg directory:{} state:{}>".format(
            self.directory, json.dumps(self.state))
        
    # private methods follow 

    def __parse_value_param(self, value_param):
        if value_param.lower() in VALID_FORMATS:
            return value_param.lower()
        else:
            return None

    def __parse_generation_number(self, f):
        print('__parse_generation_number: {}'.format(f))
        match = re.search(RE_GENERATIION_NUMBER, f)
        print(match)
        if match != None:
            span = match.span()
            if span != None:
                print('span[0] {}'.format(span[0]))
                print('span[1] {}'.format(span[1]))
                numpart = f[span[0]:span[1]]
                print('numpart: {}'.format(numpart))
                return int(numpart)
        return -1

    def __format_regexp(self):
        format_template = self.state['pattern'].replace('%', '{}')
        format_values = list()
        re_value = RE_TOKEN_MAP[self.state['value_param']] 
        format_values.append(re_value)
        return format_template.format(*format_values)

    def __walk_fs(self):
        files = list()
        for dir_name, subdirs, base_names in os.walk(self.directory):
            for base_name in base_names:
                relative_path = "{}/{}".format(dir_name, base_name)
                files.append(relative_path)
        return sorted(files)

    def __read_state(self):
        try:
            with open(self.metafile, 'rt') as f:
                return json.loads(f.read())
        except:
            return {}

    def __write_state(self):
        with open(self.metafile, 'w') as f:
            jstr = json.dumps(self.state)
            f.write(jstr)
            if self.verbose:
                print('state:{}'.format(jstr))
