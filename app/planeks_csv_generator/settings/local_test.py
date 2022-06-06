# Test settings. These are settings used by the test runner.
from dj_database_url import config as db_config

from .base import *  # noqa

DEBUG = True
LOCAL_LOGIN = True

# Set DJANGODB_URL='postgres://<user>@<host>/<db_name>' for postgres
DATABASES = {
    'default': db_config(default='sqlite:///:memory:'),
}
