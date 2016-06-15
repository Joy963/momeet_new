#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .index import bp as index_bp


def register_routes(app, url_prefix='/'):
    app.register_blueprint(index_bp, url_prefix=url_prefix)
    return app
