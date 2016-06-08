#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from momeet.lib import BaseModel, db
from momeet.models.industry import get_industry
from momeet.utils import utf8


USER_PER_PAGE_COUNT = 20


class NoneUser(object):
    """
    """
    username = ''

    def __str__(self):
        return 'none'

    def __repr__(self):
        return '<NonUser: none>'

    def to_dict(self):
        return dict(username=self.username)


class Privilege(BaseModel):
    """
    用户微信特权
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), default='')


class User(BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(100))  # openid
    wechat_union_id = db.Column(db.String(100))  # 微信唯一ID
    avatar = db.Column(db.String(500))  # 头像
    gender = db.Column(db.SmallInteger, default=0)  # 性别
    user_name = db.Column(db.String(40), index=True, nullable=False)  # 用户名

    real_name = db.Column(db.String(40))  # 真实姓名
    id_card = db.Column(db.String(40))  # 身份证信息
    birthday = db.Column(db.DateTime)  # 出生日期
    age = db.Column(db.Integer, default=0)  # 年龄
    height = db.Column(db.Integer, default=0)  # 身高
    mobile_num = db.Column(db.String(20), index=True)  # 手机号
    weixin_num = db.Column(db.String(100))  # 微信号

    country = db.Column(db.String(20))  # 国家
    location = db.Column(db.String(100), default='0,0')  # 所在城市

    industry_id = db.Column(db.Integer, default=0)  # 行业
    company_name = db.Column(db.String(100))  # 公司名称
    profession = db.Column(db.String(100))  # 职位
    income = db.Column(db.SmallInteger, default=0)  # 年收入

    graduated = db.Column(db.String(100))  # 毕业院校
    education = db.Column(db.SmallInteger, default=0)  # 学历

    affection = db.Column(db.SmallInteger, default=0)  # 感情状况
    hometown = db.Column(db.String(100), default='0,0')  # 家乡

    drink = db.Column(db.SmallInteger, default=0)  # 是否喝酒
    smoke = db.Column(db.SmallInteger, default=0)  # 是否抽烟
    constellation = db.Column(db.SmallInteger, default=0)  # 星座
    religion = db.Column(db.SmallInteger, default=0)  # 信仰

    is_active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.now)
    dict_default_columns = ['avatar', 'real_name', 'gender', 'user_name', 'id_card',
                            'birthday', 'age', 'height', 'location', 'affection',
                            'mobile_num', 'weixin_num', 'country', 'drink', 'smoke',
                            'hometown', 'constellation', 'religion', 'created',
                            'income', 'social_id', 'wechat_union_id', 'id']

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return utf8(self.user_name)

    def __repr__(self):
        return utf8('<User: %s>' % self.user_name)

    def to_dict_ext(self, columns=None):
        d = self.to_dict(columns=columns)
        industry = get_industry(self.industry_id)
        d['industry'] = industry.name if industry else ''
        d['work_expirence'] = map(lambda x: x.to_dict(), WorkExperience.query.filter_by(user_id=self.id).all())
        d['edu_expirence'] = map(lambda x: x.to_dict(), EduExperience.query.filter_by(user_id=self.id).all())
        return d


class WorkExperience(BaseModel):
    dict_default_columns = ["company_name", "profession", "income", "industry_id"]

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    industry_id = db.Column(db.Integer, default=0)  # 行业
    company_name = db.Column(db.String(100))  # 公司名称
    profession = db.Column(db.String(100))  # 职位
    income = db.Column(db.SmallInteger, default=0)  # 年收入


class EduExperience(BaseModel):
    dict_default_columns = ["id", "graduated", "education", "major"]

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    graduated = db.Column(db.String(100))  # 毕业院校
    education = db.Column(db.SmallInteger, default=0)  # 学历
    major = db.Column(db.String(100))   # 专业


class UserPhoto(BaseModel):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo = db.Column(db.String(3000))
    is_active = db.Column(db.Boolean, default=True)


class UserInfo(BaseModel):
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    photos = db.Column(db.String(3000))  # 照片
    description = db.Column(db.String(1000))  # 自我介绍
    auth_info = db.Column(db.String(3000))  # 认证
    detail = db.Column(db.LargeBinary)  # 详细介绍

    @classmethod
    def create(cls, user_id, photos=None, description='', detail=''):
        info = cls(user_id=user_id)
        info.photos = photos
        info.description = description
        info.detail = detail
        info.save()
        return info


class UserInvitation(BaseModel):
    """
    用户支持的邀约
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    invitation_type = db.Column(db.SmallInteger, nullable=False)
    description = db.Column(db.String(1000))  # 活动介绍
    price = db.Column(db.Integer, default=0)  # 活动价格
    is_active = db.Column(db.Boolean, default=True)


def get_user(user_id):
    if str(user_id).isdigit():
        return User.query.get(user_id)
    return User.query.filter_by(social_id=user_id).first()


def get_user_by_name(user_name):
    return User.query.filter_by(user_name=user_name).first()


def get_user_by_social_id(social_id):
    return User.query.filter_by(social_id=social_id).first()


def get_user_list_by_page(page=1):
    query_kwargs = dict(is_active=True)
    users = User.query.filter_by(**query_kwargs)
    users = users.order_by(User.id.desc()).paginate(page, USER_PER_PAGE_COUNT)
    return users.items, users.total


def get_user_info(user_id):
    info = UserInfo.query.get(user_id)
    if not info:
        info = UserInfo.create(user_id)
    return info


class UserProcess(object):
    def __init__(self, openid):
        self.openid = openid
        self.user = get_user(self.openid)

    def update_avatar(self, avatar_uri):
        if not self.user:
            return False
        self.user.avatar = avatar_uri
        self.user.save()
        return avatar_uri

    def add_edu_experience(self, d):
        if not self.user:
            return False
        edu = EduExperience(user_id=self.user.id)
        for k, v in d.items():
            setattr(edu, k, v)
        return edu.save()

    def add_work_experience(self, d):
        if not self.user:
            return False
        work = WorkExperience(user_id=self.user.id)
        for k, v in d.items():
            setattr(work, k, v)
        return work.save()


class UserInfoProcess(object):

    def __init__(self, user_id):
        self.user_id = user_id

    def get_photos(self):
        return map(lambda x: x.photo, UserPhoto.query.filter_by(
            user_id=self.user_id, is_active=True).all())

    def add_photo(self, photo):
        u_p = UserPhoto(user_id=self.user_id)
        u_p.photo = photo
        u_p.save()
        return u_p

    def del_photo(self, photo):
        u_p = UserPhoto.query.filter_by(
            user_id=self.user_id, photo=photo).first()
        u_p.is_active = False
        u_p.save()
        return u_p

    def get_auth_info(self):
        info = get_user_info(self.user_id)
        return info.auth_info or []

    def save_auth_info(self, auth_info):
        info = get_user_info(self.user_id)
        info.auth_info = ''.join(auth_info)
        info.save()
