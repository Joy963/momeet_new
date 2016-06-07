#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
# import urllib2
# import cStringIO
# from itsdangerous import (
#     TimedJSONWebSignatureSerializer as Serializer,
#     BadSignature,
#     SignatureExpired
# )
from momeet.lib import (
    BaseModel, db
)
from momeet.models.industry import get_industry
# from momeet.constants.user import *
# from momeet.utils import utf8
from momeet.lib import session_scope
from momeet.utils import utf8, FancyDict, safe_int
# from momeet.utils.upload import save_avatar_to_qiniu
# from momeet.config import c


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
                            'hometown', 'constellation', 'religion', 'created']

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
        # for k, v in d.items():
        #     if k == 'affection':
        #         d[k] = USER_AFFECTION_DESC.get(v)
        #     if k == 'constellation':
        #         d[k] = CONSTELLATION_DESC.get(v)
        #     if k == 'drink':
        #         d[k] = DRINK_STATUS_DESC.get(v)
        #     if k == 'gender':
        #         d[k] = USER_GENDER_DESC.get(v)
        #     if k == 'income':
        #         d[k] = INCOME_STATUS_DESC.get(v)
        #     if k == 'smoke':
        #         d[k] = SMOKE_STATUS_DESC.get(v)
        return d

    # def generate_auth_token(self, expiration=600):
    #     s = Serializer(c.SECRET_KEY, expires_in=expiration)
    #     return s.dumps({'social_id': self.social_id})
    #
    # @staticmethod
    # def verify_auth_token(token):
    #     s = Serializer(c.SECRET_KEY)
    #     try:
    #         data = s.loads(token)
    #     except SignatureExpired:
    #         return None
    #     except BadSignature:
    #         return None
    #     return get_user_by_social_id(data['social_id'])


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

    # def _process_photo(self, process_name, photo):
    #     if not photo:
    #         return
    #     photos = self.get_photos()
    #     modify = False
    #     if process_name == 'add' and photo not in photos:
    #         photos.append(photo)
    #         modify = True
    #     if process_name == 'del' and photo in photos:
    #         photos.remove(photo)
    #         modify = True
    #
    #     if modify:
    #         for photo in photos:
    #             u_p = UserPhoto(user_id=self.user_id)
    #             u_p.photo = photo
    #             u_p.save()
    #     return photos

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

