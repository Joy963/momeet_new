#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime
from momeet.lib import BaseModel, db
from momeet.utils import FancyDict, safe_int


class Theme(BaseModel):
    dict_default_columns = ['id', 'price', 'theme']
    id = db.Column(db.Integer, primary_key=True)
    engagement_id = db.Column(db.Integer, db.ForeignKey('engagement.id'))
    theme = db.Column(db.String(100))
    price = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Theme, self).__init__(**kwargs)

    def __str__(self):
        return unicode(self.theme)

    def __repr__(self):
        return unicode('<EngagementTheme: %s>' % self.theme)

    @classmethod
    def get_theme(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()


class Engagement(BaseModel):
    """
    邀约活动
    """
    dict_default_columns = ['id', 'user_id', 'is_active', 'description', 'created']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    description = db.Column(db.String(5000))
    theme = db.relationship('Theme', backref='engagement_theme', lazy='dynamic')

    is_active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.now())

    @classmethod
    def get_engagement(cls, uid, **kwargs):
        return cls.query.filter_by(user_id=uid, is_active=True, **kwargs).order_by(cls.created.desc()).all()


class UserEngagementProcess(object):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_all_engagement(self):
        return Engagement.query.filter_by(
            user_id=self.user_id, is_active=True).order_by(Engagement.id.desc()).all()

    def get_all_engagement_dict(self):
        _all = self.get_all_engagement()
        data = map(lambda _: FancyDict(theme=map(lambda x: FancyDict(
                theme=safe_int(x.theme), price=x.price), _.theme.filter_by(engagement_id=_.id).all()),
                description=_.description, user_id=_.user_id), _all)
        return data[0] if data else FancyDict(user_id=self.user_id)

    # def save_invitation(self, theme_list, price, description=''):
    #     theme_list = [safe_int(_) for _ in theme_list if safe_int(_)]
    #     for invitation_type in theme_list:
    #         invitation = UserInvitation.query.filter_by(user_id=self.user_id, invitation_type=int(invitation_type)).first()
    #         if not invitation:
    #             invitation = UserInvitation(user_id=self.user_id, invitation_type=safe_int(invitation_type))
    #         invitation.description = description
    #         invitation.price = safe_int(price)
    #         invitation.is_active = True
    #         invitation.save()
    #         with session_scope() as db_session:
    #             db_session.query(UserInvitation).filter(
    #                 UserInvitation.user_id == self.user_id,
    #                 ~UserInvitation.invitation_type.in_(theme_list)
    #             ).update(
    #                 dict(is_active=False),
    #                 synchronize_session='fetch'
    #             )

