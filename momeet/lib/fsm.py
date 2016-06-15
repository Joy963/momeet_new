#!/usr/bin/python
# coding:utf-8


class FiniteStateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, status, handler, end_state=0):

        self.handlers[status] = handler
        if end_state:
            self.endStates.append(status)

    def set_start(self, status):
        self.startState = status

    def run(self, status, action, **kargs):
        # try:
        handler = self.handlers[status]
        # except:
        #     raise InitializationError("must call has a start state")
        return handler(action, **kargs)


def confirm_transition(action, **kwargs):
    pass


def cancle_transition(action, **kwargs):
    pass
