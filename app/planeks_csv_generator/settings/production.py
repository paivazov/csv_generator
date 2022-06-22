"""
isort:skip_file
"""
# Production-only settings. Uses config to get live values
# from os import environ

from .base import *  # noqa
from dj_database_url import config as db_config

# CUSTOMER environment variable specifies the customer name if we are a single

#  tenant site instance.
# SECRET_KEY = environ['DJANGO_SECRET_KEY']
SECRET_KEY = 'django-insecure-96u8@5duj)x3_%-w9*6af7h^p#8!hao3*8b)i^ql+v))x2k8'

# databases are dynamically provided at runtime
DATABASES = {
    'default': db_config(default='sqlite:///:memory:'),
}
