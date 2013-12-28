#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from pyqp.aggregate import Accumulative
from pyqp.reducers import last, nvl


def _nvl(self, *args):
    return nvl(args)

def _create_column(self, config):
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
        self._columns = columns
        self._rows = defaultdict(self._init_row)

    def _init_row(self, key):
        return OrderedDict((c.name, c) for c in \
                                            map(_create_column, self._columns))

    def add_value(self, row, column, value):
        self._rows[row][column].append(value)
        return self

    @property
    def columns(self):
        return self._columns

    def __iter__(self):
        return self._rows.values()


class Column(object):

    def __init__(self, name, reducer=None, handler=None, desc=None, type=None, \
                 start_value=None):
        self.name = name
        self.desc = _nvl(desc, name)
        self.type = _nvl(type, 'str')
        self.reducer = _nvl(reducer, last)
        # using 'if' statement to avoid creating objects if not necessary
        self.handler = (handler if handler is not None else Accumulative(60))()
        self.start_value = _nvl(start_value, 0)

    def __str__(self):
        return reduce(self.reducer, self.handler, self.start_value)

    def append(self, value):
        self.handler.append(value)
        return self
