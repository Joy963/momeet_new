#!/usr/bin/env python
# -*- coding: utf-8 -*-


from wtforms import StringField, IntegerField, FieldList, validators
from momeet.models.invitation import get_invitation_code
from momeet.forms.base import BaseForm
from momeet.models.user import User
from momeet.lib.database import db


class UserSocialIdForm(BaseForm):
    openid = StringField(u'第三方标识ID', [validators.required()])

    def __init__(self, *args, **kwargs):
        super(UserSocialIdForm, self).__init__(*args, **kwargs)

    @staticmethod
    def openid_check(openid):
        return User.query.filter_by(social_id=openid).first() is not None


class NewUserForm(BaseForm):
    code = StringField(u'邀请码', [validators.required()])
    openid = StringField(u'普通用户标识', [validators.required()])
    nickname = StringField(u'用户昵称', [validators.required()])
    head_img_url = StringField(u'头像', [validators.required()])
    union_id = StringField(u'用户统一标识', [validators.required()])

    sex = IntegerField(u'性别')
    province = StringField(u'省份')
    city = StringField(u'城市')
    country = StringField(u'国家')

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

    def save(self):
        if User.query.filter_by(social_id=self.openid.data).first():
            return None
        invitation_code = get_invitation_code(self.code.data)
        if not invitation_code:
            return None
        invitation_code.is_used = True
        user = User()
        user.social_id = self.openid.data
        user.user_name = self.nickname.data
        user.gender = self.sex.data
        user.location = '{},{}'.format(self.province.data, self.city.data)
        user.country = self.country.data
        user.avatar = self.head_img_url.data
        user.wechat_union_id = self.union_id.data

        invitation_code.save()
        user.save()
        return user



