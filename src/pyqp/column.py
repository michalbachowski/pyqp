#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import copy
from pyqp.aggregate import Accumulate
from pyqp.reducers import last, nvl


def _nvl(*args):
    return nvl(args)


def column_factory(config):
    # so maybe config is valid Column instance?
    try:
        config.name
        config.desc
        config.type_name
        config.append
        config.__copy__
        config.__str__
    except AttributeError:
        pass
    else:
        return copy(config)

    # is column config a dict?
    try:
        return Column(**config)
    except TypeError:
        pass

    # is column config a tuple?
    try:
        return Column(*config)
    except TypeError:
        pass

    # is column config a string?
    try:
        return Column(config)
    except TypeError:
        pass

    # I give up...
    raise ValueError("Expected valid column configuration or instance, got %s" \
                                                                    % config)


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

    def __str__(self):
        raise NotImplementedError()

    def __copy__(self):
        raise NotImplementedError()


class Column(Abstract):

    def __init__(self, name, reducer=None, handler_factory=None, desc=None, \
                                            type_name=None, default_value=None):
        Abstract.__init__(self, name, _nvl(desc, name), _nvl(type_name, 'str'))
        self._reducer = _nvl(reducer, last)
        self._default_value = str(_nvl(default_value, 0))
        self._handler_factory = _nvl(handler_factory, Accumulate(60))
        self._handler = self._handler_factory()

    def __copy__(self):
        return Column(self.name, self._reducer, self._handler_factory, \
                    self.desc, self.type_name, self._default_value)

    def __str__(self):
        if len(self._handler) == 0:
            return self._default_value
        return str(self._reducer(self._handler))

    def append(self, value):
        self._handler.append(value)
        return self
