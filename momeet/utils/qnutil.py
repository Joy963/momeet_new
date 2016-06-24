#!usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from werkzeug.utils import secure_filename
from flask import current_app
from qiniu import Auth, put_data

from .common import get_random_string, compatmd5

from momeet.lib import rdb


def get_qiniu_default_config():
    field_default_dict = {
        'access_key': 'QINIU_ACCESS_KEY',
        'secret_key': 'QINIU_SECRET_KEY',
        'image_host': 'QINIU_IMAGE_HOST',
        'bucket_name': 'QINIU_IMAGE_BUCKET',
        'cut_suffix_format': 'QINIU_IMAGE_CUT_SUFFIX'
    }
    default_config = dict()
    for field, config_name in field_default_dict.iteritems():
        default_config[field] = current_app.config[config_name]
    return default_config


class QiniuHelper(object):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    def __init__(self, **kwargs):
        # 没有传递配置过来，则获取默认配置。这里这么做其实也是为了便于task中使用此类。
        if not kwargs:
            kwargs = get_qiniu_default_config()
        self.init_config(kwargs)
        self.client = Auth(self.access_key, self.secret_key)
        self.token_key = 'momeet_{bucket_name}_qi_niu_upload_token'.format(
            bucket_name=self.bucket_name
        )

    def init_config(self, kwargs):
        for field, value in kwargs.iteritems():
            setattr(self, field, value)

    def get_upload_token(self):
        token = rdb.get(self.token_key)
        if not token:
            policy = {
                'returnBody': '{"key": $(key), "hash": $(etag), "image": $(imageInfo)}'
            }
            qn = self.client
            token = qn.upload_token(self.bucket_name, policy=policy)
            rdb.setex(self.token_key, 3000, token)
        return token

    def upload(self, file_name, file_data):
        image_host = self.image_host
        token = self.get_upload_token()
        ret, info = put_data(token, file_name, file_data)
        if info.status_code == 200:
            return_url = image_host + ret.get('key')
            image = ret.get('image', {})
            if image:
                cut_suffix = self.cut_suffix_format.format(
                    width=image.get('width'),
                    height=image.get('height')
                )
                return_url = return_url + cut_suffix
            return return_url

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def upload_img(self, file):
        filename = file.filename
        if not self.allowed_file(filename):
            return ''
        file_suffix = os.path.splitext(secure_filename(filename))[-1].lower()
        filename = compatmd5(get_random_string() + secure_filename(filename) + str(time.time())) + file_suffix
        return self.upload(filename, file.stream)

    def upload_avator(self, file_name, file_data):
        if not self.allowed_file(file_name):
            return ''
        file_suffix = os.path.splitext(secure_filename(file_name))[-1].lower()
        file_name = compatmd5(get_random_string() + secure_filename(file_name) + str(time.time())) + file_suffix
        return self.upload(file_name, file_data)


def get_qiniu_img_w_h(image_url):
    # http://7vzrwi.com1.z0.glb.clouddn.com/f4b00c5b471014d8103f5457a9fcd43b.gif?imageMogr/v2/thumbnail/130x153
    data = image_url.split('/')[-1]
    w, h = data.split('x')
    return w, h
