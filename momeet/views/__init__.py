#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from flask import g, request


from .dashboard import (
    regist_routes as dash_reg_routes,
    resources as dash_resources,
    error_handlers as dash_err_hanlders
)
from .api import (
    register_routes as api_reg_routes,
    before_request as api_before_request
)
# from .web import (
#     register_routes as web_routes,
#     before_request as web_before_request,
#     resources as web_resources,
#     error_handlers as web_error_handlers
# )


def register_views(app):
    dash_reg_routes(app)
    if app.is_api:
        api_reg_routes(app)
    # # if app.is_web:
    #     web_routes(app)


def before_request(app):
    g.request_start_time = int(time.time() * 1000)
    # if app.is_web:
    #     web_before_request(app)
    if app.is_api:
        api_before_request(app)


def after_request(response):
    path = request.path
    if path.startswith('/static/') or path == '/favicon.ico':
        return response
    return response


def resources(app):
    # if app.is_web:
    dash_resources(app)
    if app.is_api:
        pass


def error_handlers(app):
    if app.is_api:
        pass
    else:
        dash_err_hanlders(app)
