from dj_database_url import config as db_config

from .base import *  # noqa

DEBUG = True
LOCAL_LOGIN = True

# export DJANGODB_URL='...' and/or WAREHOUSE_URL for a different DB app
DATABASES = {
    'default': db_config(default='sqlite:///:memory:'),
}

STATIC_ROOT = Path(BASE_DIR).parent.joinpath('var', 'static')
