from django.conf import settings

from zru import ZRUClient as ZRUClientPython


__title__ = 'ZRU Django'
__version__ = '1.0.0'
__author__ = 'ZRU'
__license__ = 'BSD 2-Clause'
__copyright__ = 'Copyright 2017 ZRU'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'

default_app_config = 'zru_django.apps.ZRUDjangoConfig'


class ZRUClient(ZRUClientPython):
    """
    Wrapper of ZRUClient of Python
    """
    def __init__(self):
        """
        Initializes a ZRUClient getting key and secret key from DB
        """

        try:
            key = settings.ZRU_CONFIG['PUBLIC_KEY']
            secret_key = settings.ZRU_CONFIG['SECRET_KEY']
        except:
            key = ''
            secret_key = ''
        super(ZRUClient, self).__init__(key, secret_key)
