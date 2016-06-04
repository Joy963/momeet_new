from flask import Blueprint, request, json
from ._base import BaseView
from momeet.models.invitation import (
    create_invitation_code,
    code_check
)


bp = Blueprint('invitation', __name__)


class GetInvitationCode(BaseView):
    def get(self):
        code = create_invitation_code()
        return json.dumps({"code": code.to_dict(
            ['id', 'code', 'is_used', 'created']), "success": True})


class InvitationCodeCheck(BaseView):
    def post(self):
        data = json.loads(request.data)
        return json.dumps({"success": code_check(data.get('code'))})


bp.add_url_rule("check/", view_func=InvitationCodeCheck.as_view("invitation.check"))
bp.add_url_rule("code/", view_func=GetInvitationCode.as_view("code.get"))
