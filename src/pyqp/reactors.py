#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Abstract(object):

    def append(self, event_handler):
        return self

    def emit(self, event_name, data):
        return self

    def process(self):
        return self


class Local(Abstract):

    def __init__(self):
        self._handlers = []

    def append(self, event_handler):
        self._handlers.append(event_handler)
        return self

    def emit(self, event_name, data):
        for handler in self._handlers:
            handler.dispatch(event_name, data)
        return self

    def process(self):
        for handler in self._handlers:
            handler.process()
        return self
