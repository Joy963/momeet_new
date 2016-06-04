from flask import Blueprint, json, request, g
from ._base import BaseView
from momeet.models.user import (
    get_user_by_social_id,
    User
)
from momeet.lib import auth

bp = Blueprint('account', __name__)


class OldUserExistCheck(BaseView):
    def post(self):
        data = json.loads(request.data)
        return json.dumps({"success": get_user_by_social_id(data.get('openid')) is not None})


class NewUserInfoCreate(BaseView):
    def post(self):
        data = json.loads(request.data)
        user = User.create_or_update(**data)
        g.user = user
        return json.dumps({"success": True, "uid": user.id})


class NewUserInfoUpdate(BaseView):
    @auth.login_required
    def post(self):
        data = json.loads(request.data)
        user = User.create_or_update(**data)
        return json.dumps({"success": True, "uid": user.id})


class TestView(BaseView):
    @auth.login_required
    def get(self):
        return "Api View Test!"


bp.add_url_rule("user/check", view_func=OldUserExistCheck.as_view("user.check"))
bp.add_url_rule("user/create", view_func=NewUserInfoCreate.as_view("user.create"))
bp.add_url_rule("user/update", view_func=NewUserInfoUpdate.as_view("user.update"))
bp.add_url_rule("test", view_func=TestView.as_view("test"))
