from flask import Blueprint, jsonify
from ._base import BaseView
from momeet.models.engagement import Engagement
from momeet.forms.engagement import EngagementForm
# from momeet.models.user import get_user
from momeet.models.engagement import UserEngagementProcess


bp = Blueprint('engagement', __name__)


class EngagementView(BaseView):
    def get(self, uid):
        return jsonify({
            "success": True,
            "results": map(lambda x: dict(x.to_dict(), theme=map(lambda y: y.to_dict(), x.theme.all())),
                           Engagement.get_engagement(uid))
        })

    def post(self, uid):
        _obj = UserEngagementProcess(uid).get_all_engagement_dict()
        form = EngagementForm(csrf_enabled=False, obj=_obj)
        if form.validate_on_submit() and form.save():
            return jsonify({"success": True})
        return jsonify({"success": False})


bp.add_url_rule("<string:uid>/", view_func=EngagementView.as_view("info"))
