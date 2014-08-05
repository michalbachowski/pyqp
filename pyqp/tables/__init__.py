#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from operator import methodcaller


class Table(object):

    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self._rows = defaultdict(self._init_row)
        self._values_extractor = methodcaller('values')

    def _init_row(self):
        return OrderedDict((c.name, c.duplicate()) for c in self.columns)

    def add_value(self, row, column, value):
        self._rows[row][column].append(value)
        return self

    def remove_row(self, key):
        del self._rows[key]
        return self

    def __iter__(self):
        return iter(map(self._values_extractor, self._rows.values()))
