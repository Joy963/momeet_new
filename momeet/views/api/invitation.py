from flask import Blueprint, request, jsonify
from ._base import BaseView
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
            return jsonify({"success": form.code_check()})
        return jsonify({"success": False})


bp.add_url_rule("check/", view_func=InvitationCodeCheck.as_view("check"))
bp.add_url_rule("code/", view_func=GetInvitationCode.as_view("code"))
