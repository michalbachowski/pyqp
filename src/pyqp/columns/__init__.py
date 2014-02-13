#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyqp.aggregate import LastValue
from pyqp.reducers import last


class Column(object):

    def __init__(self, name, reducer=last, handler_factory=LastValue,
                 desc=None, type_name='str', default_value=0):
        self._name = name
        self._desc = desc if desc is not None else name
        self._type_name = type_name
        self._reducer = reducer
        self._default_value = default_value
        self._handler_factory = handler_factory
        self._handler = self._handler_factory()

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def type_name(self):
        return self._type_name

    def duplicate(self):
        """Makes duplicate of itself *without any data*

        @return Column"""
        return Column(self.name, self._reducer, self._handler_factory, \
                    self.desc, self.type_name, self._default_value)

    def reduce(self):
        iterable = list(self._handler)
        if len(iterable) == 0:
            return self._default_value
        return self._reducer(iterable)

    def __str__(self):
        return str(self.reduce())

    def append(self, value):
        self._handler.append(value)
        return self
