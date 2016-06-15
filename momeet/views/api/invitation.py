#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
from momeet.views.base import BaseView
from momeet.forms.invitation import InvitationCodeForm
from momeet.models.invitation import create_invitation_code


bp = Blueprint('invitation', __name__)


class GetInvitationCode(BaseView):
    def get(self):
        code = create_invitation_code()
        return jsonify({"code": code.to_dict(), "success": True})


class InvitationCodeCheck(BaseView):
    def post(self):
        form = InvitationCodeForm(csrf_enabled=False)
        if form.validate_on_submit():
            r = form.code_check()
            return jsonify({"success": r[0], "msg": {"title": r[1], "content": r[2]}})
        return jsonify({"success": False, "msg": {"title": u"邀请码已过期", "content": u"请输入正确有效的邀请码"}})


bp.add_url_rule("check", view_func=InvitationCodeCheck.as_view("check"))
bp.add_url_rule("code", view_func=GetInvitationCode.as_view("code"))
