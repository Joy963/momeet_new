#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import (
    abort, request
)
from flask.views import View


class BaseView(View):
    methods = ['GET', 'POST']

    def dispatch_request(self, *args, **kwargs):
        request_method = request.method
        method = getattr(self, request_method.lower())(*args, **kwargs)
        return method

    def get(self, *args, **kwargs):
        abort(405)

    def post(self, *args, **kwargs):
        abort(405)


