#!/usr/bin/env python
# -*- coding: utf-8 -*-


from wtforms import validators, IntegerField, TextAreaField
from momeet.forms.base import BaseForm
from momeet.models.engagement import Engagement, Theme
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
