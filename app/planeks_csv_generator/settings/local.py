from dj_database_url import config as db_config

from .base import *  # noqa

DEBUG = True
LOCAL_LOGIN = True

DATABASES = {
    'default': db_config(
        env=DJANGODB_URL, default='sqlite:///:memory:'  # noqa: F405
    ),
}

STATIC_ROOT = Path(BASE_DIR).parent.joinpath('var', 'static')  # noqa: F405
