#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtforms import StringField, validators
from momeet.forms.base import BaseForm
from momeet.models.invitation import InvitationCode
from momeet.utils.error import ErrorsEnum


class InvitationCodeForm(BaseForm):
    code = StringField(u'邀请码', [validators.required()])

    def __init__(self, *args, **kwargs):
        super(InvitationCodeForm, self).__init__(*args, **kwargs)

    def code_check(self):
        code = InvitationCode.query.filter_by(code=self.code.data).first()
        if not code or code and code.code != self.code.data:
            return False, ErrorsEnum.INVITATION_CODE_NON_EXIST.describe(), u"请输入正确有效的邀请码"
        if code and code.is_used:
            return False, ErrorsEnum.INVITATION_CODE_INVALID.describe(), u"请输入正确有效的邀请码"
        return True, u"OK", u"OK"

