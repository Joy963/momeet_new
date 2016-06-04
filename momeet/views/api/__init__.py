#!/usr/bin/env python
# -*- coding: utf-8 -*-


from .account import bp as account_bp
from .invitation import bp as invitation_bp
from .user_info import bp as user_bp
from .auth_token import bp as auth_bp


def register_routes(app, url_prefix='/api/'):
    app.register_blueprint(account_bp, url_prefix=url_prefix + 'account/')
    app.register_blueprint(invitation_bp, url_prefix=url_prefix + 'invitation/')
    app.register_blueprint(user_bp, url_prefix=url_prefix + 'user/')
    app.register_blueprint(auth_bp, url_prefix=url_prefix + 'auth/')


def before_request(app):
    pass
