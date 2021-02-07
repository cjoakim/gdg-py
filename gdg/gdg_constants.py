__author__ = 'cjoakim'


class Constants(object):

    @classmethod
    def format_generation(cls):
        return 'g'

    @classmethod
    def format_epoch(cls):
        return 'e'

    @classmethod
    def format_timestamp_utc(cls):
        return 'ts_utc'

    @classmethod
    def format_timestamp_local(cls):
        return 'ts_local'

    @classmethod
    def valid_formats(cls):
        return [
            Constants.format_generation(),
            Constants.format_epoch(),
            Constants.format_timestamp_utc(),
            Constants.format_timestamp_local()
        ]

    @classmethod
    def generation_format(cls):
        return '{0:06d}'

    @classmethod
    def timestamp_format(cls):
        return '%Y-%m-%d-%H:%M:%S'

    @classmethod
    def parameter_char(cls):
        return '%'

    @classmethod
    def re_generation_number(cls):
        return '\\d\\d\\d\\d\\d\\d'

    @classmethod
    def re_token_map(cls):
        d = dict()
        d[Constants.format_generation()]      = '\\d\\d\\d\\d\\d\\d'  # 6 digits
        d[Constants.format_epoch()]           = '\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d'  # 10 digits
        d[Constants.format_timestamp_utc()]   = '\\d\\d\\d\\d-\\d\\d-\\d\\d-\\d\\d:\\d\\d:\\d\\d'  # 2021-02-05-07:56:23
        d[Constants.format_timestamp_local()] = '\\d\\d\\d\\d-\\d\\d-\\d\\d-\\d\\d:\\d\\d:\\d\\d'  # 2021-02-05-07:56:23
        return d 
