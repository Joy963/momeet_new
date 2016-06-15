#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from momeet.lib import BaseModel, db
from momeet.utils import utf8, Pagination
from momeet.utils.common import FancyDict
from sqlalchemy import or_


USER_PER_PAGE_COUNT = 20


def get_job_label_or_create(**kwargs):
    return JobLabel.query.filter_by(**kwargs).first() or JobLabel(**kwargs)


def get_job_label_list_by_page(page=1, **kwargs):
    labels = JobLabel.query.filter_by(**kwargs).paginate(page, USER_PER_PAGE_COUNT)
    pagination = Pagination(page, USER_PER_PAGE_COUNT, labels.total)
    return labels.items, pagination


def get_personal_label_or_create(**kwargs):
    return PersonalLabel.query.filter_by(**kwargs).first() or PersonalLabel(**kwargs)


def get_personal_label_list_by_page(page=1, **kwargs):
    labels = PersonalLabel.query.filter_by(**kwargs).paginate(page, USER_PER_PAGE_COUNT)
    pagination = Pagination(page, USER_PER_PAGE_COUNT, labels.total)
    return labels.items, pagination


class JobLabel(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class PersonalLabel(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


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

    longtitude = db.Column(db.Float)    # 经度
    laititude = db.Column(db.Float)  # 纬度

    engagement = db.relationship('Engagement', backref='user_engagement', lazy='dynamic')
    edu = db.relationship('EduExperience', backref='user_edu_experience', lazy='dynamic')
    work = db.relationship('WorkExperience', backref='user_work_experience', lazy='dynamic')
    photo = db.relationship('UserPhoto', backref='user_photo', lazy='dynamic')
    job_label = db.relationship('JobLabel', backref='user_job_label', lazy='dynamic')
    personal_label = db.relationship('PersonalLabel', backref='user_personal_label', lazy='dynamic')

    industry = db.Column(db.SmallInteger, default=0)  # 行业
    income = db.Column(db.SmallInteger, default=0)  # 年收入
    affection = db.Column(db.SmallInteger, default=0)  # 感情状况
    hometown = db.Column(db.String(100), default='0,0')  # 家乡
    drink = db.Column(db.SmallInteger, default=0)  # 是否喝酒
    smoke = db.Column(db.SmallInteger, default=0)  # 是否抽烟
    constellation = db.Column(db.SmallInteger, default=0)  # 星座
    religion = db.Column(db.SmallInteger, default=0)  # 信仰

    device_token = db.Column(db.String(100))    # 设备token
    app_version = db.Column(db.String(30))  # app 版本
    mobile_model = db.Column(db.String(50))  # 手机型号
    os_version = db.Column(db.String(30))   # os 版本
    system_language = db.Column(db.String(30))  # 系统语言

    is_active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.now)
    dict_default_columns = ['avatar', 'real_name', 'gender', 'user_name', 'id_card',
                            'birthday', 'age', 'height', 'location', 'affection',
                            'mobile_num', 'weixin_num', 'country', 'drink', 'smoke',
                            'hometown', 'constellation', 'religion', 'created',
                            'social_id', 'wechat_union_id', 'id', 'industry', 'income']

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return unicode(self.user_name)

    def __repr__(self):
        return unicode('<User: %s>' % self.user_name)

    def to_dict_ext(self, columns=None):
        d = self.to_dict(columns=columns)
        completeness, msg, next_page = get_user_info_completeness(self.id)
        d['completeness'] = {
            'completeness': completeness,
            'msg': msg,
            'next_page': next_page
        }
        d['job_label'] = ','.join(map(lambda x: x.name, self.job_label.all()))
        d['personal_label'] = ','.join(map(lambda x: x.name, self.personal_label.all()))
        d['birthday'] = d.get('birthday')[:10]
        d['work_expirence'] = map(lambda x: x.to_dict(), self.work.all())
        d['edu_expirence'] = map(lambda x: x.to_dict(), self.edu.all())
        return d

    def to_dict_index(self):
        columns = ['real_name', 'gender', 'longtitude', 'laititude']
        d = self.to_dict(columns=columns)
        d['job_label'] = ','.join(map(lambda x: x.name, self.job_label.all()))
        d['personal_label'] = ','.join(map(lambda x: x.name, self.personal_label.all()))
        user_info = UserInfo.query.get(self.id)
        d['cover_photo'] = user_info.cover_photo
        return d


class WorkExperience(BaseModel):
    dict_default_columns = ["id", "company_name", "profession", "created", "user_id"]

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_name = db.Column(db.String(100))  # 公司名称
    profession = db.Column(db.String(100))  # 职位
    created = db.Column(db.DateTime, default=datetime.now())

    @classmethod
    def get_work_experience(cls, wid):
        return WorkExperience.query.get(wid)


class EduExperience(BaseModel):
    dict_default_columns = ["id", "graduated", "education", "major", "created", "user_id"]

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    graduated = db.Column(db.String(100))  # 毕业院校
    education = db.Column(db.SmallInteger, default=0)  # 学历
    major = db.Column(db.String(100))   # 专业
    created = db.Column(db.DateTime, default=datetime.now())

    @classmethod
    def get_edu_experience(cls, eid):
        return EduExperience.query.get(eid)


class UserPhoto(BaseModel):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo = db.Column(db.String(3000))
    is_active = db.Column(db.Boolean, default=True)


class UserDetail(BaseModel):
    dict_default_columns = ['id', 'title', 'content', 'photo']
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_info_id = db.Column(db.Integer, db.ForeignKey('user_info.user_id'))
    title = db.Column(db.String(300))
    content = db.Column(db.String(3000))
    photo = db.Column(db.Text)

    def to_dict_ext(self, columns=None):
        d = self.to_dict(columns)
        d['photo'] = d.get('photo').split(',')
        return d


class UserInfo(BaseModel):
    dict_default_columns = ['user_id', 'description', 'auth_info', 'cover_photo']
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    description = db.Column(db.String(1000))  # 个人亮点
    auth_info = db.Column(db.String(3000))  # 认证
    detail = db.relationship('UserDetail', backref='user_detail', lazy='dynamic')  # 详细介绍
    cover_photo = db.Column(db.String(1000))  # 封面照片

    @classmethod
    def create(cls, user_id, photos=None, description='', detail=''):
        info = cls(user_id=user_id)
        info.photos = photos
        info.description = description
        info.detail = detail
        info.save()
        return info


def get_user(user_id):
    if not user_id:
        return None
    if str(user_id).isdigit():
        return User.query.get(user_id)
    return User.query.filter_by(social_id=user_id).first()


def get_all_user():
    return User.query.order_by(User.id.asc()).all()


def get_user_by_name(user_name):
    return User.query.filter_by(user_name=user_name).first()


def get_user_by_social_id(social_id):
    return User.query.filter_by(social_id=social_id).first()


def get_user_list_by_page(page=1, **kwargs):
    users = User.query.filter(or_(getattr(User, k) == v for k, v in kwargs.items()))\
        .filter_by(is_active=True)
    users = users.order_by(User.id.desc()).paginate(page, USER_PER_PAGE_COUNT)
    return users.items, users.total


def get_user_list_limit(limit=20, **kwargs):
    users = User.query.filter(or_(getattr(User, k) == v for k, v in kwargs.items())) \
        .filter_by(is_active=True)
    return users.order_by(User.id.desc()).limit(limit=limit).all()


def get_user_info(user_id):
    user = get_user(user_id)
    if not user:
        return None
    info = UserInfo.query.get(user.id)
    if not info:
        info = UserInfo.create(user.id)
    return info


def get_user_info_completeness(user_id=None):
    complete = 0
    msg = u''
    next_page = 0
    user = get_user(user_id)
    user_info = UserInfo.query.get(user.id)
    if not user:
        return complete, msg

    user_dict = user.to_dict()
    user_info_dict = user_info.to_dict() if user_info else FancyDict()
    base_info = ['avatar', 'real_name', 'gender', 'birthday',
                 'height', 'mobile_num', 'weixin_num', 'location']

    ext_info = ['industry', 'income', 'affection', 'hometown',
                'constellation']

    other_info = ['edu', 'work', 'job_label',
                  'user_description', 'user_cover_photo',
                  'user_detail']

    base_complete = len(filter(lambda _: _ in user_dict.keys() and user_dict.get(_), base_info))
    ext_complete = len(filter(lambda _: _ in user_dict.keys() and user_dict.get(_), ext_info))

    job_label_flag = False
    description_flag = False
    detail_flag = False

    for _ in other_info:
        if _ == 'edu' and user.edu.all():
            complete += 1
        if _ == 'work' and user.work.all():
            complete += 1
        if _ == 'job_label':
            if getattr(user, _).all():
                complete += 1
                job_label_flag = True
            else:
                msg = u'职业标签还未编辑哦'
                next_page = 2
        if _ == 'user_description':
            if user_info_dict.description:
                complete += 1
                description_flag = True
            else:
                msg = u'编辑个人亮点后可上首页哦'
                next_page = 3
        if _ == 'user_cover_photo' and user_info_dict.cover_photo:
            complete += 1
        if _ == 'user_detail':
            if user_info.detail.count() > 1:
                complete += 1
                detail_flag = True
            else:
                msg = u'完善更多介绍约见成功率更高哦'
                next_page = 4

    if ext_complete <= 3:
        msg = u'完善资料开始约见吧'
        next_page = 1
    elif job_label_flag and description_flag and detail_flag:
        msg = ','.join(map(lambda x: x.name, user.job_label.all()))

    complete = int((complete + base_complete + ext_complete)*100.0/
                   len(base_info + ext_info + other_info))
    return complete, msg, next_page


class UserProcess(object):
    def __init__(self, openid):
        self.openid = openid
        self.user = get_user(self.openid)

    def update_avatar(self, avatar_uri):
        if not self.user:
            return None
        self.user.avatar = avatar_uri
        self.user.save()
        return avatar_uri

    def add_edu_experience(self, d):
        if not self.user:
            return None
        edu = EduExperience(user_id=self.user.id)
        for k, v in d.items():
            setattr(edu, k, v)
        return edu.save()

    def update_edu_experience(self, d, eid):
        if not self.user:
            return None
        edu = EduExperience.get_edu_experience(eid)
        if not edu:
            return None
        for k, v in d.items():
            setattr(edu, k, v)
        return edu.save()

    def add_work_experience(self, d):
        if not self.user:
            return None
        work = WorkExperience(user_id=self.user.id)
        for k, v in d.items():
            setattr(work, k, v)
        return work.save()

    def update_work_experience(self, d, wid):
        if not self.user:
            return None
        work = WorkExperience.get_work_experience(wid)
        if not work:
            return None
        for k, v in d.items():
            setattr(work, k, v)
        return work.save()


class UserInfoProcess(object):

    def __init__(self, user_id):
        self.user_id = user_id
        self.user = get_user(self.user_id)

    def update_cover_photo(self, photo_uri):
        if not self.user:
            return None
        user_info = UserInfo.query.get(self.user.id)
        user_info.cover_photo = photo_uri
        user_info.save()
        return photo_uri

    def get_userinfo(self):
        if not self.user:
            return None
        return UserInfo.query.get(self.user.id)

    def get_details(self):
        user_info = UserInfo.query.get(self.user.id)
        return user_info.detail.all()

    def del_detail(self, did):
        d = UserDetail.query.get(did)
        return d.delete() if d else None

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
