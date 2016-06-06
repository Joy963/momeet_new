#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
import urllib2
import cStringIO
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)
from momeet.lib import (
    BaseModel, db
)
from momeet.utils import utf8
from momeet.lib import session_scope
from momeet.utils import FancyDict, safe_int
from momeet.utils.upload import save_avatar_to_qiniu
from momeet.config import c


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

    affection = db.Column(db.SmallInteger, default=0)  # 感情状况
    graduated = db.Column(db.String(100))  # 毕业院校
    education = db.Column(db.SmallInteger, default=0)  # 学历
    hometown = db.Column(db.String(100), default='0,0')  # 家乡

    drink = db.Column(db.SmallInteger, default=0)  # 是否喝酒
    smoke = db.Column(db.SmallInteger, default=0)  # 是否抽烟
    constellation = db.Column(db.SmallInteger, default=0)  # 星座
    religion = db.Column(db.SmallInteger, default=0)  # 信仰

    is_active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.now)
    dict_default_columns = ['avatar', 'real_name', 'gender',
                            'birthday', 'height', 'location', 'affection',
                            'mobile_num', 'weixin_num', 'industry_id',
                            'income', 'hometown', 'constellation']

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return utf8(self.user_name)

    def __repr__(self):
        return utf8('<User: %s>' % self.user_name)

    def generate_auth_token(self, expiration=600):
        s = Serializer(c.SECRET_KEY, expires_in=expiration)
        return s.dumps({'social_id': self.social_id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(c.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return get_user_by_social_id(data['social_id'])

    @classmethod
    def create_or_update(cls, **kwargs):
        user = cls.query.filter_by(social_id=kwargs.get("openid")).first() or User()
        user.social_id = kwargs.get("openid")
        user.user_name = kwargs.get("nickname")
        head_img_url = kwargs.get("head_img_url")
        file_data = cStringIO.StringIO(urllib2.urlopen(head_img_url).read())
        file_name = user.social_id + ".jpg"

        user.avatar = save_avatar_to_qiniu(file_name, file_data)
        user.wechat_union_id = kwargs.get("union_id")

        user.gender = kwargs.get("sex")
        user.location = "{},{}".format(kwargs.get("province"),
                                       kwargs.get("province"))
        user.country = kwargs.get("country")
        db.session.add(user)
        db.session.commit()
        return user


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
        db.session.add(self.user)
        db.session.commit()
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
        info = get_user_info(self.user_id)
        return info.photos or []

    def _process_photo(self, process_name, photo):
        if not photo:
            return
        photos = self.get_photos()
        modify = False
        if process_name == 'add':
            if photo not in photos:
                photos.append(photo)
                modify = True
        else:
            if photo in photos:
                photos.remove(photo)
                modify = True
        if modify:
            info = get_user_info(self.user_id)
            info.photos = photos
            info.save()
        return photos

    def add_photo(self, photo):
        return self._process_photo('add', photo)

    def del_photo(self, photo):
        return self._process_photo('del', photo)

    def get_auth_info(self):
        info = get_user_info(self.user_id)
        return info.auth_info or []

    def save_auth_info(self, auth_info):
        info = get_user_info(self.user_id)
        info.auth_info = ''.join(auth_info)
        info.save()


class UserInvitationProcess(object):

    def __init__(self, user_id):
        self.user_id = user_id

    def get_all_invitation(self):
        _all = UserInvitation.query.filter_by(
            user_id=self.user_id, is_active=True).order_by(UserInvitation.id.desc()).all()
        return _all

    def get_all_invitation_dict(self):
        _all = self.get_all_invitation()
        data = FancyDict()
        invitation_type_list = []
        desc = u''
        price = 0
        for _ in _all:
            invitation_type_list.append(_.invitation_type)
            desc = _.description
            price = _.price

        data['price'] = price
        data['description'] = desc
        data['invitation_type_list'] = invitation_type_list
        data['user_id'] = self.user_id
        return data

    def save_invitation(self, invitation_type_list, price, description=''):
        invitation_type_list = [safe_int(_) for _ in invitation_type_list if safe_int(_)]
        for invitation_type in invitation_type_list:
            invitation = UserInvitation.query.filter_by(user_id=self.user_id, invitation_type=int(invitation_type)).first()
            if not invitation:
                invitation = UserInvitation(user_id=self.user_id, invitation_type=safe_int(invitation_type))
            invitation.description = description
            invitation.price = safe_int(price)
            invitation.is_active = True
            invitation.save()
            with session_scope() as db_session:
                db_session.query(UserInvitation).filter(
                    UserInvitation.user_id == self.user_id,
                    ~UserInvitation.invitation_type.in_(invitation_type_list)
                ).update(
                    dict(is_active=False),
                    synchronize_session='fetch'
                )

