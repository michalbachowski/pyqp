#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from .column import column_factory as default_column_factory


class Abstract(object):

    def __init__(self, name, columns, column_factory=None, *args, **kwargs):
        self.name = name
        self._columns_conf = columns
        self._column_factory = column_factory if column_factory is not None \
                                                    else default_column_factory
        self._columns = list(self._create_columns_list())

    def _create_columns_list(self):
        return map(self._column_factory, self._columns_conf)

    def add_value(self, row, column, value):
        pass

    @property
    def columns(self):
        return self._columns

    def __iter__(self):
        return iter([])


class TableForwarder(Abstract):

    def __init__(self, proxy, name, columns):
        self._proxy = proxy
        Abstract.__init__(self, name, columns)

    def add_value(self, row, column, value):
        self._proxy.send('pyqp_cell_value', (self.name, row, column, value))


class Table(Abstract):

    def __init__(self, name, columns):
        Abstract.__init__(self, name, columns)
        self._rows = defaultdict(self._init_row)

    def _init_row(self):
        return OrderedDict((c.name, c) for c in self._create_columns_list())

    def add_value(self, row, column, value):
        self._rows[row][column].append(value)
        return self

    def __iter__(self):
        return iter(self._rows.values())
