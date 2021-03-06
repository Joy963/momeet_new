#!/usr/bin/env python
# -*- coding: utf-8 -*-


from wtforms import validators, IntegerField, TextAreaField, StringField
from momeet.forms.base import BaseForm
from momeet.models.user import get_user
from momeet.models.engagement import Engagement, Theme, EngagementOrder, get_engagement_order
from momeet.utils.view import MultiCheckboxField
from .fields_name import UserFields
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

    def save(self, theme_data=None):
        # TODO bug 传入空值
        if not theme_data:
            theme_data = self.theme.data

        uid = self._obj.user_id if self._obj and self._obj.user_id else None

        engagements = Engagement.get_engagement(uid)
        engagement = engagements[0] if engagements else Engagement()
        engagement.user_id = uid
        engagement.description = self.description.data

        for t in Theme.get_theme(engagement_id=engagement.id):
            t.delete()

        if not self.description.data or theme_data == ['']:
            try:
                engagement.delete()
            except:
                return False
        else:
            engagement.save()

        for _ in theme_data:
            theme = Theme()
            theme.engagement_id = engagement.id
            theme.price = 50
            theme.theme = _
            theme.save()

        return True


class EngagementOrderForm(BaseForm):
    host = IntegerField(UserFields.INVITATION_HOST)
    guest = IntegerField(UserFields.INVITATION_GUEST)
    description = TextAreaField(UserFields.INVITATION_DESC)
    theme = StringField(UserFields.INVITATION_TYPE)

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

