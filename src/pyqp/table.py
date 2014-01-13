#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from pyqp.column import column_factory as default_column_factory
from operator import methodcaller


class Abstract(object):

    def __init__(self, name, columns, column_factory=default_column_factory, \
                                                            *args, **kwargs):
        self.name = name
        self._columns_conf = columns
        self._column_factory = column_factory
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
        return iter(map(methodcaller('values'), self._rows.values()))

class TableForwarder(Abstract):

    def __init__(self, proxy, name, columns):
        self._proxy = proxy
        Abstract.__init__(self, name, columns)

    def add_value(self, row, column, value):
        self._proxy.send('pyqp_cell_value', (self.name, row, column, value))

class TableFilterable(Abstract):

    def __init__(self, base_table, col_filter, row_filter):
        self._table = base_table
        self._col_filter = col_filter if col_filter is not None else self._true
        self._row_filter = row_filter if row_filter is not None else self._true

    def _true(self, *args, **kwargs):
        return True

    @property
    def name(self):
        return self._table.name

    @property
    def columns(self):
        return self._filter_columns(self._table.columns)

    def __iter__(self):
        return map(self._filter_columns, filter(self._row_filter, self._table))

    def _filter_columns(self, row):
        return (col for col in row if self._col_filter(col.name))
