from flask import Blueprint, json, request, g
from ._base import BaseView
from momeet.models.user import (
    get_user,
    EduExperience,
    WorkExperience
)
from momeet.forms.user import (
    UserForm,
    UserInfoUpdateForm,
    UserAvatarForm,
    UserEduInfoForm,
    UserWorkInfoForm
)

bp = Blueprint('user_info', __name__)


class UserBaseInfo(BaseView):
    def get(self, uid):
        user = get_user(uid)
        return json.dumps(user.to_dict() if user else {})

    def post(self, uid):
        form = UserInfoUpdateForm(csrf_enabled=False)
        if form.validate_on_submit() and form.save(uid):
            return json.dumps({"success": True})
        return json.dumps({"success": False})


class UserAvatar(BaseView):
    def post(self, uid):
        form = UserAvatarForm(csrf_enabled=False)
        if form.validate_on_submit():
            avatar_uri = form.save(uid)
            if avatar_uri:
                return json.dumps({"success": True, "avatar": avatar_uri})
        return json.dumps({"success": False, "msg": "failed update avatar!"})


class UserEduInfo(BaseView):
    def get(self, uid):
        user = get_user(uid)
        if not user:
            return json.dumps({"success": False, "msg": "invalid uid or openid!"})
        edus = EduExperience.query.filter_by(user_id=user.id)
        return json.dumps({"success": True, "results": [_.to_dict() for _ in edus]})

    def post(self, uid):
        user = get_user(uid)
        if not user:
            return json.dumps({"success": False, "msg": "invalid uid or openid!"})
        form = UserEduInfoForm(csrf_enabled=False)
        if form.validate_on_submit() and form.save(uid):
            return json.dumps({"success": True, "msg": "add edu exprience success"})
        return json.dumps({"success": False, "msg": "add edu exprience failed"})


class UserWorkInfo(BaseView):
    def get(self, uid):
        user = get_user(uid)
        if not user:
            return json.dumps({"success": False, "msg": "invalid uid or openid!"})
        works = WorkExperience.query.filter_by(user_id=user.id)
        return json.dumps({"success": True, "results": [_.to_dict() for _ in works]})

    def post(self, uid):
        user = get_user(uid)
        if not user:
            return json.dumps({"success": False, "msg": "invalid uid or openid!"})
        form = UserWorkInfoForm(csrf_enabled=False)
        if form.validate_on_submit() and form.save(uid):
            return json.dumps({"success": True, "msg": "add work exprience success"})
        return json.dumps({"success": False, "msg": "add work exprience failed"})


bp.add_url_rule("avatar/<string:uid>", view_func=UserAvatar.as_view("avatar"))
bp.add_url_rule("base_info/<string:uid>", view_func=UserBaseInfo.as_view("base_info"))
bp.add_url_rule("edu_info/<string:uid>", view_func=UserEduInfo.as_view("edu_info"))
bp.add_url_rule("work_info/<string:uid>", view_func=UserWorkInfo.as_view("work_info"))
