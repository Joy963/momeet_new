from flask import Blueprint, json, request, g
from ._base import BaseView
from momeet.lib import auth
from momeet.models.user import (
    get_user_by_social_id,
    User
)

bp = Blueprint('user_info', __name__)


class GetUserBaseInfo(BaseView):
    def get(self, openid):
        user = get_user_by_social_id(openid)
        return json.dumps(user.to_dict() if user else {})


bp.add_url_rule("info/<string:openid>", view_func=GetUserBaseInfo.as_view("base_info"))
