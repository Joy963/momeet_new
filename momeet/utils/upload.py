#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .qnutil import QiniuHelper

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload_file_to_qiniu(file):
    helper = QiniuHelper()
    src = helper.upload_img(file)
    return src


def save_avatar_to_qiniu(file_name, file_data):
    helper = QiniuHelper()
    return helper.upload_avator(file_name, file_data)
