#!/usr/bin/env python
# -*- coding: utf-8 -*-


from enum import IntEnum, unique


@unique
class ErrorsEnum(IntEnum):
    INDUSTRY_NAME_REQUIRED = 200001
    INDUSTRY_NAME_EXISTS = 200002

    USER_NAME_REQUIRED = 200003
    USER_NAME_EXISTS = 200004
    USER_SOCIAL_ID_EXISTS = 2000013

    HEIGHT_ERROR = 200005
    LOCATION_ERROR = 200006
    HOMETOWN_ERROR = 200007
    IMAGE_ERROR = 200008

    PHOTO_REQUIRED = 200009
    INVITATION_TYPE_REQUIRED = 200010

    INVITATION_CODE_REQUIRED = 200011

    SOCIAL_ID_REQUIRED = 200012

    def describe(self):
        return _ERRORS.get(self)


_ERRORS = {
    ErrorsEnum.INDUSTRY_NAME_REQUIRED: u"请输入行业名称",
    ErrorsEnum.INDUSTRY_NAME_EXISTS: u"已存在相同行业",

    ErrorsEnum.USER_NAME_REQUIRED: u"请输入用户名",
    ErrorsEnum.USER_NAME_EXISTS: u"已存在相同用户名",
    ErrorsEnum.USER_SOCIAL_ID_EXISTS: u"已存在相同OPENID",

    ErrorsEnum.HEIGHT_ERROR: u"身高输入错误",
    ErrorsEnum.LOCATION_ERROR: u"所在地输入错误",
    ErrorsEnum.HOMETOWN_ERROR: u"家乡输入错误",

    ErrorsEnum.IMAGE_ERROR: u"图片格式错误",
    ErrorsEnum.PHOTO_REQUIRED: u"请选择要上传的照片",
    ErrorsEnum.INVITATION_TYPE_REQUIRED: u"请选择邀约类型",
    # TODO 提示信息
    ErrorsEnum.INVITATION_CODE_REQUIRED: u"邀请码缺失",
    ErrorsEnum.SOCIAL_ID_REQUIRED: u"SOCIAL_ID缺失",
}
