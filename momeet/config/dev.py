#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ._base import ApiConfig, WebConfig

all = ['DevApiConfig', 'DevWebConfig']


class DevMixin(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://dev:123456@127.0.0.1:3306/momeet?charset=utf8mb4"

    # 连接池
    SQLALCHEMY_POOL_SIZE = 10
    # 连接池重连时间
    SQLALCHEMY_POOL_RECYCLE = 3000

    RUN_ENV = 'dev'
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True

    # redis
    REDIS_DB = 2
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'ecang_redis$%^'


class DevApiConfig(DevMixin, ApiConfig):
    def __init__(self):
        self.LOGGERS['momeet']['level'] = 'DEBUG'
        self.LOGGERS['momeet']['file'] = './logs/dev/api.log'


class DevWebConfig(DevMixin, WebConfig):
    def __init__(self):
        self.LOGGERS['momeet']['level'] = 'DEBUG'
        self.LOGGERS['momeet']['file'] = './logs/dev/web.log'
