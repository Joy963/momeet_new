#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import hashlib
from flask import url_for, request, make_response
from flask_wtf.csrf import CsrfProtect

from momeet.utils import to_unicode, safe_int, logger

from .misc import bp as dashboard_bp
from .user import bp as user_bp
from .account import bp as account_bp


def regist_routes(app, url_prefix='/dashboard/'):
    app.register_blueprint(dashboard_bp, url_prefix=url_prefix)
    app.register_blueprint(user_bp, url_prefix=url_prefix + 'user/')
    app.register_blueprint(account_bp, url_prefix=url_prefix + 'account/')


def before_request(app):
    pass


def resources(app):
    # TODO csrf
    # csrf = CsrfProtect()
    # csrf.init_app(app)
    if not hasattr(app, '_static_hash'):
        app._static_hash = {}

    def static_file(filename):
        c = app.config
        run_env = c.get('RUN_ENV', 'local')
        prefix = c.get('SITE_STATIC_PREFIX', '/static/')
        if run_env == 'local':
            value = '%s%s' % (prefix, filename)
        else:
            if filename in app._static_hash:
                return app._static_hash[filename]
            try:
                with open(os.path.join(app.static_folder, filename), 'r') as f:
                    content = f.read()
                    hsh = hashlib.md5(content).hexdigest()
                value = '%s%s?v=%s' % (prefix, filename, hsh[:5])
            except:
                value = '%s%s' % (prefix, filename)
            app._static_hash[filename] = value
        return value

    def url_for_page(page, endpoint=None, params=None):
        args = dict(request.args.copy())
        args['page'] = page
        args.update(request.view_args)
        if params:
            args.update(params)
        if not endpoint:
            endpoint = request.endpoint
        return url_for(endpoint, **args)

    def url_for_args(**kwargs):
        args = request.args.copy()
        for k, v in kwargs.iteritems():
            args[k] = v
        return url_for(request.endpoint, **args)

    @app.context_processor
    def register_context():
        return dict(
            static_file=static_file,
            url_for_args=url_for_args,
            to_unicode=to_unicode
        )

    app.jinja_env.globals['url_for_page'] = url_for_page
    app.jinja_env.globals['int'] = safe_int
    app.jinja_env.globals['safe_int'] = safe_int
    app.jinja_env.globals['str'] = str


def error_handlers(app):
    def internal_error(error):
        logger.error(error, exc_info=True)
        resp = make_response("Internal Server Error", 500)
        sentry = app.extensions.get('sentry', None)
        if sentry:
            sentry.captureException()
        return resp
    app.register_error_handler(Exception, internal_error)
