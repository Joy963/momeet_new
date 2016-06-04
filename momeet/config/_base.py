#!/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseConfig(object):
    APP_NAME = "momeet"
    DEBUG = False
    TESTING = False
    SITE_URL = '/'
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    #: session
    SESSION_COOKIE_NAME = 'momeet_session_id'
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 15
    SESSION_REFRESH_EACH_REQUEST = True

    #: account
    SECRET_KEY = 'MOMEET_SECRET_KEY_!@#$'
    PASSWORD_SECRET = 'MOMEET_PASSWORD_SECRET_!)!%'
    RESERVED_WORDS = [
        'root', 'admin', 'bot', 'robot', 'master', 'webmaster',
        'account', 'people', 'user', 'users', 'project', 'projects',
        'search', 'action', 'favorite', 'like', 'love', 'none',
        'team', 'teams', 'group', 'groups', 'organization',
        'organizations', 'package', 'packages', 'org', 'com', 'net',
        'help', 'doc', 'docs', 'document', 'documentation', 'blog',
        'bbs', 'forum', 'forums', 'static', 'assets', 'repository',
        'public', 'private', 'mac', 'windows', 'ios', 'lab', u'管理员'
    ]

    LOGGERS = {
        'momeet': {
            'level': 'INFO',
        },
    }

    QINIU_ACCESS_KEY = '58H9P7Z9RbwaLwc7QNMR-wwGFbMaL0TvuCOVWgQZ'
    QINIU_SECRET_KEY = '7UWMoQbeVTzVRJuWox7B2w4x4-vfrlU9bzicds3D'
    QINIU_IMAGE_BUCKET = 'momeetdev'  # 图片空间
    QINIU_IMAGE_HOST = 'http://7xsatk.com1.z0.glb.clouddn.com/'  # 访问域名
    QINIU_IMAGE_CUT_SUFFIX = '?imageMogr/v2/thumbnail/{width}x{height}'


class ApiConfig(BaseConfig):
    PROJECT = 'API'


class WebConfig(BaseConfig):
    PROJECT = 'WEB'
