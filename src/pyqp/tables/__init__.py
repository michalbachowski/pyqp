#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from operator import methodcaller
from pyqp.columns.factory import default_column_factory


class Table(object):

    def __init__(self, name, columns, column_factory=default_column_factory, \
                                                            *args, **kwargs):
        self.name = name
        self._columns_conf = columns
        self._column_factory = column_factory
        self.columns = list(self._create_columns_list())
        self._rows = defaultdict(self._init_row)
        self._values_extractor = methodcaller('values')

    def _create_columns_list(self):
        return map(self._column_factory, self._columns_conf)

    def _init_row(self):
        return OrderedDict((c.name, c) for c in self._create_columns_list())

    def add_value(self, row, column, value):
        self._rows[row][column].append(value)
        return self

    def remove_row(self, key):
        del self._rows[key]
        return self

    def __iter__(self):
        return iter(map(self._values_extractor, self._rows.values()))
