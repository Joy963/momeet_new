#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, json
from momeet.views.base import BaseView
from momeet.models.engagement import (
    Engagement,
    EngagementOrder,
    UserEngagementProcess,
    get_engagement_order_list,
    get_engagement_order
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
        theme = request.form.getlist('theme')
        if form.validate_on_submit() and form.save(theme=theme):
            return jsonify({"success": True})
        return jsonify({"success": False})


class EngagementOrderView(BaseView):
    """
    邀约订单
    """
    def get(self, oid=None):
        if oid:
            order = get_engagement_order(oid)
            return jsonify({"success": True, "order": order.to_dict() if order else {}})

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


class EngagementOrderStatusView(BaseView):
    actions = ['confirm', 'deny', 'cancel', 'pay']

    def post(self, oid):
        try:
            params = json.loads(request.data)
        except ValueError:
            params = {}

        order = get_engagement_order(oid)
        user = get_user(params.get('user_id'))
        action = params.get('action')
        if not order or not user or not action:
            return jsonify({"success": False, "msg": "invalid order_id or user_id"})
        user_id = user.id

        status_change_result = False
        if action == 'confirm' and user_id == order.host:  # host确认
            status_change_result = status_transition(order, 1, 4)

        if action == 'deny' and user_id == order.host:  # host拒绝
            status_change_result = status_transition(order, 1, 3)
            if not status_change_result:
                status_change_result = status_transition(order, 6, 9)
                # TODO 退款

        if action == 'cancel' and user_id == order.guest:  # guest取消
            status_change_result = status_transition(order, 1, 2)
            if not status_change_result:
                status_change_result = status_transition(order, 6, 7)
                # TODO 退款

        if action == 'pay' and user_id == order.guest:  # guest支付
            # TODO pay with alpay
            status_change_result = status_transition(order, 4, 5)

        if not status_change_result:
            return jsonify({"success": status_change_result, "msg": "invalid status transition"})

        order.save()
        return jsonify({"success": True, "order": order.to_dict()})


def status_transition(order, status_from, status_to):
    if order.status == status_from:
        order.status = status_to
        order.save()
        return True
    else:
        return False



#
# class EngagementOrderStatus(object):
#     def __init__(self, order_id):
#         self.obj = get_engagement_order(order_id)
#
#
# class OrderGuestStartStatus(EngagementOrderStatus):
#     def run(self):
#         self.obj.status = 1
#         self.obj.save()
#
#
# class OrderHostConfirmStatus(EngagementOrderStatus):
#     def host_apply(self):
#         pass
#
#     def host_deny(self):
#         pass
#
#     def guest_cancle(self):
#         pass
#
#
# class OrderGuestPayStatus(EngagementOrderStatus):
#     pass
#
#
# class OrderPayConfirmStatus(EngagementOrderStatus):
#     pass
#
#
# class OrderToMeetStatus(EngagementOrderStatus):
#     pass
#
#
# class OrderCompleteStatus(EngagementOrderStatus):
#     pass


bp.add_url_rule("list/<string:uid>/", view_func=EngagementView.as_view("list"))
bp.add_url_rule("order/<string:oid>", view_func=EngagementOrderView.as_view("order"))

bp.add_url_rule("order_action/<string:oid>", view_func=EngagementOrderStatusView.as_view("order.action"))
