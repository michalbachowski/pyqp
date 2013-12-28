#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from pyqp.aggregate import Accumulative
from pyqp.reducers import last, nvl


def _nvl(*args):
    return nvl(args)

def _create_column(config):
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
    # it has to be string... otherwise I give up :(
    return Column(config)


class Table(object):

    def __init__(self, name, columns):
        self.name = name
        self._columns_conf = columns
        self._columns = list(self._create_columns_list())
        self._rows = defaultdict(self._init_row)

    def _init_row(self):
        return OrderedDict((c.name, c) for c in self._create_columns_list())

    def _create_columns_list(self):
        return map(_create_column, self._columns_conf)

    def add_value(self, row, column, value):
        self._rows[row][column].append(value)
        return self

    @property
    def columns(self):
        return self._columns

    def __iter__(self):
        return iter(self._rows.values())


class Column(object):

    def __init__(self, name, reducer=None, handler=None, desc=None, type=None, \
                 default_value=None):
        self.name = name
        self.desc = _nvl(desc, name)
        self.type = _nvl(type, 'str')
        self.reducer = _nvl(reducer, last)
        self.default_value = str(_nvl(default_value, 0))
        # using 'if' statement to avoid creating objects if not necessary
        self.handler = (handler if handler is not None else Accumulative(60))()

    def __str__(self):
        if len(self.handler) == 0:
            return self.default_value
        return str(self.reducer(self.handler))

    def append(self, value):
        self.handler.append(value)
        return self
