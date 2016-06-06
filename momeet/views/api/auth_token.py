from flask import Blueprint, g
from ._base import BaseView
from momeet.lib import auth
from momeet.models.user import User

bp = Blueprint('auth', __name__)


# @auth.verify_token
# def verify_token(token):
#     user = User.verify_auth_token(token)
#     # if not user:
#     #     return False
#     #     # try to authenticate with username/password
#     #     # user = User.query.filter_by(username=username_or_token).first()
#     #     # if not user or not user.verify_password(password):
#     #     #     return False
#     g.user = user
#     return True


class GenAuthToken(BaseView):
    @auth.login_required
    def get(self):
        return g.user.generate_auth_token()


bp.add_url_rule("token", view_func=GenAuthToken.as_view("token"))


