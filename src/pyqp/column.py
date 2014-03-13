#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyqp.aggregate import LastValue
from pyqp.reducers import last


class Column(object):

    def __init__(self, name, reducer=last, handler=None, desc=None,
                                            type_name='str', default_value=0):
        self.name = name
        self.desc = desc if desc is not None else name
        self.type_name = type_name
        self._reducer = reducer
        self._default_value = default_value
        self._handler = handler if handler is not None else LastValue()

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

    def duplicate(self):
        """
        Creates duplicate of current column instance *with empty handler*
        """
        return Column(self.name, self._reducer, self._handler.duplicate(),
                      self.desc, self.type_name, self._default_value)
