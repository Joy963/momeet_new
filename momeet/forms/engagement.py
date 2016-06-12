#!/usr/bin/env python
# -*- coding: utf-8 -*-


from wtforms import validators, IntegerField, TextAreaField, StringField
from momeet.forms.base import BaseForm
from momeet.models.user import get_user
from momeet.models.engagement import Engagement, Theme, EngagementOrder
from momeet.utils.view import MultiCheckboxField
from .fields_name import UserFields
from momeet.utils.error import ErrorsEnum
from momeet.constants.user import InvitationTypeEnum


class EngagementForm(BaseForm):
    description = TextAreaField(UserFields.INVITATION_DESC, [validators.required()])
    price = IntegerField(UserFields.INVITATION_PRICE, default=50)
    theme = MultiCheckboxField(UserFields.INVITATION_TYPE)

    def __init__(self, *args, **kwargs):
        super(EngagementForm, self).__init__(*args, **kwargs)
        self.price.data = 50
        _choices = [(str(_.value), _.describe()) for _ in sorted(InvitationTypeEnum.__members__.values())]
        self.theme.choices = _choices
        if self._obj and self._obj.theme:
            self.theme.checked_list = [int(_.theme) for _ in self._obj.theme]

    def save(self):
        uid = self._obj.user_id if self._obj and self._obj.user_id else None

        engagements = Engagement.get_engagement(uid)
        engagement = engagements[0] if engagements else Engagement()
        engagement.user_id = uid
        engagement.description = self.description.data
        engagement.save()

        for t in Theme.get_theme(engagement_id=engagement.id):
            t.delete()

        for _ in self.theme.data:
            theme = Theme()
            theme.engagement_id = engagement.id
            theme.price = 50
            theme.theme = _
            theme.save()
        return engagement


class EngagementOrderForm(BaseForm):
    host = IntegerField(UserFields.INVITATION_HOST, [validators.required()])
    guest = IntegerField(UserFields.INVITATION_GUEST, [validators.required()])
    description = TextAreaField(UserFields.INVITATION_DESC, [validators.required()])
    theme = StringField(UserFields.INVITATION_TYPE, [validators.required()])

    def validate_host(self, field):
        data = field.data
        if not data:
            return
        try:
            int(data)
        except:
            raise ValueError(ErrorsEnum.HEIGHT_ERROR.describe())

    def validate_guest(self, field):
        data = field.data
        if not data:
            return
        try:
            int(data)
        except:
            raise ValueError(ErrorsEnum.HEIGHT_ERROR.describe())

    def save(self, theme=None):
        host = get_user(self.host.data)
        guest = get_user(self.guest.data)
        if not host or not guest:
            return None
        order = EngagementOrder()
        order.host = host.id
        order.guest = guest.id
        order.theme = ','.join(theme)
        order.description = self.description.data
        order.status = 1
        return order.save()
