#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._base import ApiConfig, WebConfig

all = ['LocalApiConfig', 'LocalWebConfig']


class LocalMixin(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://dev:123456@127.0.0.1:3306/momeet"
    RUN_ENV = 'local'
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True
    REDIS_DB = 3
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'ecang_redis$%^'
    STATIC_DOMIN = '/static/'
    DEBUG_TB_PROFILER_ENABLED = True


class LocalApiConfig(LocalMixin, ApiConfig):
    def __init__(self):
        self.LOGGERS['momeet']['level'] = 'DEBUG'
        self.LOGGERS['momeet']['file'] = './logs/local/api.log'


class LocalWebConfig(LocalMixin, WebConfig):
    def __init__(self):
        self.LOGGERS['momeet']['level'] = 'INFO'
        self.LOGGERS['momeet']['file'] = './logs/local/web.log'

