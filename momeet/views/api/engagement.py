#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, json
from momeet.views.base import BaseView
from momeet.models.engagement import (
    Engagement,
    EngagementOrder,
    UserEngagementProcess,
    get_engagement_order_list
)
from momeet.models.user import get_user
from momeet.forms.engagement import (
    EngagementForm,
    EngagementOrderForm
)
from momeet.utils.common import safe_int


bp = Blueprint('engagement', __name__)


class EngagementView(BaseView):
    """
    约见活动
    """
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


class EngagementOrderView(BaseView):
    """
    邀约订单
    """
    def get(self):
        status = safe_int(request.args.get("status", 0))
        host = safe_int(request.args.get("host", 0))
        guest = safe_int(request.args.get("guest", 0))
        items = get_engagement_order_list(status=status, host=host, guest=guest)
        return jsonify({"success": True, "results": map(lambda x: x.to_dict_ext(), items)})

    def post(self):
        order_form = EngagementOrderForm(csrf_enabled=False)
        if order_form.validate_on_submit():
            order = order_form.save(request.form.getlist('theme'))
            return jsonify(order.to_dict() if order else {})
        return "End"


bp.add_url_rule("list/<string:uid>/", view_func=EngagementView.as_view("list"))
bp.add_url_rule("order/", view_func=EngagementOrderView.as_view("order"))
