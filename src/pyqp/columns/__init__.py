#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from pyqp.aggregate import LastValue
from pyqp.reducers import last, nvl


def _nvl(*args):
    return nvl(args)


class Abstract(object):

    def __init__(self, name, desc, type_name, *args, **kwargs):
        self._name = name
        self._desc = desc
        self._type_name = type_name

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._desc

    @property
    def type_name(self):
        return self._type_name

    def append(self, value):
        raise NotImplementedError()

    def reduce(self):
        raise NotImplementedError()

    def __str__(self):
        return str(self.reduce())

    def __copy__(self):
        raise NotImplementedError()


class Column(Abstract):

    def __init__(self, name, reducer=None, handler_factory=None, desc=None, \
                                            type_name=None, default_value=None):
        Abstract.__init__(self, name, _nvl(desc, name), _nvl(type_name, 'str'))
        self._reducer = _nvl(reducer, last)
        self._default_value = str(_nvl(default_value, 0))
        self._handler_factory = _nvl(handler_factory, LastValue)
        self._handler = self._handler_factory()

    def __copy__(self):
        return Column(self.name, self._reducer, self._handler_factory, \
                    self.desc, self.type_name, self._default_value)

    def reduce(self):
        iterable = list(self._handler)
        if len(iterable) == 0:
            return self._default_value
        return self._reducer(iterable)

    def append(self, value):
        self._handler.append(value)
        return self
