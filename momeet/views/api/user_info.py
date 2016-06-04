from flask import Blueprint, json, request, g
from ._base import BaseView
from momeet.lib import auth
from momeet.models.user import (
    get_user_by_social_id,
    get_user
)
from momeet.forms.user import UserAvatarForm

bp = Blueprint('user_info', __name__)


class GetUserBaseInfo(BaseView):
    def get(self, uid):
        if uid.isdigit():
            user = get_user(uid)
        else:
            user = get_user_by_social_id(uid)
        return json.dumps(user.to_dict() if user else {})


class UpdataUserAvatar(BaseView):
    def post(self, uid):
        form = UserAvatarForm(csrf_enabled=False)
        if form.validate_on_submit():
            avatar_uri = form.save(uid)
            if avatar_uri:
                return json.dumps({"success": True, "avatar": avatar_uri})
        return json.dumps({"success": False, "msg": "failed update avatar!"})


bp.add_url_rule("info/<string:uid>", view_func=GetUserBaseInfo.as_view("base_info"))
bp.add_url_rule("avatar/<string:uid>", view_func=UpdataUserAvatar.as_view("avatar"))
