__author__ = 'cjoakim'


class Constants(object):

    @classmethod
    def format_generation(cls):
        return 'g'

    @classmethod
    def format_epoch(cls):
        return 'e'

# FORMAT_GENERATION = 'g'
# FORMAT_EPOCH      = 'e'
# FORMAT_TIMESTAMP_UTC = 'ts_utc'
# FORMAT_TIMESTAMP_LOCAL = 'ts_local'
# VALID_FORMATS = [
#     FORMAT_GENERATION,
#     FORMAT_EPOCH,
#     FORMAT_TIMESTAMP_UTC,
#     FORMAT_TIMESTAMP_LOCAL
# ]

# TIMESTAMP_FORMAT = '%Y-%m-%d-%H:%M:%S'

# PARAMETER_CHAR = '%'

# RE_TOKEN_MAP = dict()
# RE_TOKEN_MAP[FORMAT_GENERATION] = '\d\d\d\d\d\d'  # 6 digits
# RE_TOKEN_MAP[FORMAT_EPOCH]      = '\d\d\d\d\d\d\d\d\d\d'  # 10 digits
# RE_TOKEN_MAP[FORMAT_TIMESTAMP_UTC]   = '\d\d\d\d-\d\d-\d\d-\d\d:\d\d:\d\d'  # 2021-02-05-07:56:23
# RE_TOKEN_MAP[FORMAT_TIMESTAMP_LOCAL] = '\d\d\d\d-\d\d-\d\d-\d\d:\d\d:\d\d'  # 2021-02-05-07:56:23

# RE_GENERATIION_NUMBER = '\d\d\d\d\d\d'
