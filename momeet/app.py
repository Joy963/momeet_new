#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
from flask import Flask
from sqlalchemy.exc import InternalError

from momeet.utils.log import enable_logging
from momeet.config import c
from momeet.lib import (
    db, rdb, lm,
    RedisSessionInterface
)
from momeet.views import *


_app_instances = dict()


class MomeetAPP(Flask):
    DEBUG_TB = False

    def init_config(self):
        self.config.from_object(c)

    def init_loggers(self):
        pass
        for k, v in self.config['LOGGERS'].items():
            logger = logging.getLogger(k)
            l = v.get("level")
            f = v.get("file")
            logger.setLevel(getattr(logging, l.upper(), logging.INFO))
            enable_logging(logger, f)

    def init_db(self):
        db.init_app(self)
        db.app = self

    def init_redis(self):
        rdb.init_app(self)

    def register_routes(self):
        register_views(self)

    def init_login(self):
        lm.init_app(self)

    def register_hooks(self):
        @self.before_request
        def before():
            before_request(self)

        @self.after_request
        def after(response):
            return after_request(response)

    def register_error_handlers(self):
        def sqlalchemy_error_handler(error):
            db.session.flush()
            db.session.remove()
            raise error

        self.register_error_handler(InternalError, sqlalchemy_error_handler)
        error_handlers(self)

    def register_resources(self):
        resources(self)

    @property
    def is_api(self):
        return self.config.get('PROJECT').lower() == 'api'

    @property
    def is_web(self):
        return self.config.get('PROJECT').lower() == 'web'

    @property
    def is_local(self):
        return self.config.get('RUN_ENV').lower() == 'local'

    @property
    def is_prod(self):
        return self.config.get('RUN_ENV').lower() == 'prod'

    @property
    def is_dev(self):
        return self.config.get('RUN_ENV').lower() == 'dev'

    def register_sentry(self):
        pass


def create_app(test_config=None):
    config = os.environ.get('RUN_ENV', '')
    app = _app_instances.get(config, {}).get('app', None)
    if app:
        return app

    app = MomeetAPP(__name__)
    app.init_config()
    app.init_loggers()

    if test_config:
        app.config.update(test_config)

    app.init_db()
    app.init_redis()

    app.register_routes()
    app.register_resources()
    app.register_error_handlers()
    app.register_hooks()

    if app.config['RUN_ENV'] != 'local':
        app.register_sentry()

    app.session_interface = RedisSessionInterface(redis=rdb, prefix="rhct_session:")  # 设置 session
    if app.is_local and app.DEBUG_TB:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)

    _app_instances[config] = {}
    _app_instances[config]['app'] = app

    return app
