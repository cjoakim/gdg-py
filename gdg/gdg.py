__author__ = 'cjoakim'

import glob
import json
import os
import re
import sys
import time
import traceback

from datetime import datetime, date, timezone

from .gdg_constants import GdgConstants


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
        try:
            if int(n) > 0:
                self.state['generations'] = int(n)
                self.__write_state()
                return True
            else:
                return False
        except:
            return False

    def get_generations(self):
        if 'generations' in self.state:
            return self.state['generations']
        else:
            return -1

    def set_pattern(self, pattern, value_param):
        # reject invalid args immediately
        if (pattern == None) or (len(pattern.strip()) < 1):
            return False
        if (value_param == None) or (len(value_param.strip()) < 1):
            return False
        if (value_param.lower().strip() in GdgConstants.valid_formats()):
            pass
        else:
            return False

        curr_state = self.__read_state()  # capture current state in case of restore

        try:
            self.state['pattern'] = pattern.strip()
            self.state['value_param'] = value_param.lower().strip()
            self.state['regexp'] = self.__format_regexp()
            self.__write_state()
            return True
        except Exception as e:
            self.state = curr_state  # restore the state from before this method invocation
            self.__write_state()
            traceback.print_exc()
            return False 

    def set_verbose(self, bool=True):
        if bool == True:
            self.verbose = True
        if bool == False:
            self.verbose = False

    def next(self):
        try:
            template = self.state['pattern'].replace(GdgConstants.parameter_char(), '{}')
            values = list()
            p = self.state['value_param']

            if p == GdgConstants.format_generation():
                f, n = self.current(), 1
                if f != None:
                    n = self.__parse_generation_number(f)
                    if n > 0:
                        n = n + 1
                    else:
                        n = 1
                values.append(GdgConstants.generation_format().format(n))

            elif p == GdgConstants.format_epoch():
                values.append(int(time.time()))

            elif p == GdgConstants.format_timestamp_utc():
                values.append(datetime.utcnow().strftime(GdgConstants.timestamp_format()))

            elif p == GdgConstants.format_timestamp_local():
                values.append(datetime.now().strftime(GdgConstants.timestamp_format()))
            else:
                return None

            basename = template.format(*values)
            return '{}{}{}'.format(self.directory, os.path.sep, basename)
        except:
            return None

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

    def all_generations(self, limited=True):
        files_list, matched_list = self.__list_directory(), list()
        compiled_re = re.compile('{}{}{}'.format(
            self.directory, os.path.sep, self.state['regexp']))
        for f in files_list:
            m = compiled_re.match(f)
            if m != None:
                matched_list.append(f)

        if limited == True:
            sorted_list = sorted(matched_list)
            index = len(sorted_list) - self.get_generations()
            return sorted(sorted_list[index:])
        else:
            return sorted(matched_list)

    def all_files(self):
        return self.__list_directory()

    def prune(self, do_deletes=False):
        # return the number of files removed from the filesystem
        retain_hash = self.__generations_hash()
        pruned_count = 0
        for f in self.all_files():
            if f not in retain_hash:
                os.remove(f)
                pruned_count = pruned_count + 1
        return pruned_count

    # dunder methods

    def __str__(self):
        return "<Gdg directory:{} state:{}>".format(
            self.directory, json.dumps(self.state))
        
    # private methods follow 

    def __parse_generation_number(self, f):
        print('__parse_generation_number: {}'.format(f))
        match = re.search(GdgConstants.re_generation_number(), f)
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
        try:
            format_template = self.state['pattern'].replace('%', '{}')
            format_values = list()
            map_key = self.state['value_param']
            re_value = GdgConstants.re_token_map()[map_key]
            format_values.append(re_value)
            return format_template.format(*format_values)
        except:
            return None

    def __list_directory(self):
        # this method intentionally omits hidden files in the directory, such as .gdg
        return sorted(glob.glob('{}/*'.format(self.directory)))

    def __generations_hash(self):
        hash = dict()
        for f in self.all_generations():
            hash[f] = True
        return hash

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
