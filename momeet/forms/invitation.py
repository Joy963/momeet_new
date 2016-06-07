#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import StringField, validators
from momeet.forms.base import BaseForm
from momeet.models.invitation import InvitationCode


class InvitationCodeForm(BaseForm):
    code = StringField(u'邀请码', [validators.required()])

    def __init__(self, *args, **kwargs):
        super(InvitationCodeForm, self).__init__(*args, **kwargs)

    def code_check(self):
        code = InvitationCode.query.filter_by(code=self.code.data).first()
        return not code.is_used if code else False

