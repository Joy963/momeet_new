from flask import Blueprint, json, request, g
from ._base import BaseView
from momeet.models.user import (
    get_user,
    User
)
from momeet.lib import lm
from momeet.forms.account import UserSocialIdForm
from momeet.forms.account import NewUserForm
from flask_login import login_required, login_user, logout_user

bp = Blueprint('account', __name__)


@lm.user_loader
def user_loader(uid):
    return get_user(uid)


class UserExistCheck(BaseView):
    def post(self):
        data = json.loads(request.data)
        return json.dumps({"success": get_user(data.get('openid')) is not None})


class UserSignIn(BaseView):
    def post(self):
        form = NewUserForm(csrf_enabled=False)
        if form.validate_on_submit():
            user = form.save()
            if user:
                return json.dumps({"success": True, "uid": user.id})
        return json.dumps({"success": False})


class UserLogin(BaseView):
    def post(self):
        form = UserSocialIdForm(csrf_enabled=False)
        if form.validate_on_submit():
            user = get_user(form.openid.data)
            if user:
                login_user(user)
                return json.dumps({"success": True, "uid": user.id})
        return json.dumps({"success": False})


class UserLogout(BaseView):
    def post(self):
        return json.dumps({"success": logout_user()})


class TestView(BaseView):
    @login_required
    def get(self):
        return "<h1>Api View Test!</h1>"


bp.add_url_rule("user/check", view_func=UserExistCheck.as_view("user.check"))
bp.add_url_rule("user/signin", view_func=UserSignIn.as_view("user.signin"))
bp.add_url_rule("user/login", view_func=UserLogin.as_view("user.login"))
bp.add_url_rule("user/logout", view_func=UserLogout.as_view("user.logout"))
bp.add_url_rule("test", view_func=TestView.as_view("test"))
