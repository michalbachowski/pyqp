#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict, OrderedDict
from operator import methodcaller
from time import time
from pyqp.columns.factory import default_column_factory


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
        return self

    @property
    def columns(self):
        return self._columns

    def remove_row(self, row):
        pass

    def __iter__(self):
        return iter([])


class Table(Abstract):

    def __init__(self, *args, **kwargs):
        Abstract.__init__(self, *args, **kwargs)
        self._rows = defaultdict(self._init_row)
        self._values_extractor = methodcaller('values')

    def _init_row(self):
        return OrderedDict((c.name, c) for c in self._create_columns_list())

    def add_value(self, row, column, value):
        self._rows[row][column].append(value)
        return self

    def __iter__(self):
        return iter(map(self._values_extractor, self._rows.values()))

    def remove_row(self, key):
        del self._rows[key]
        return self


class TableTimeLimit(Table):
    """Table that prunes old rows after given amount of seconds.

    >>> from time import sleep
    >>> t = TableTimeLimit(1, 'foo', ['a'])
    >>> t.add_value(1, 'a', 11) #doctest: +ELLIPSIS
    <__init__.TableTimeLimit object at 0x...>
    >>> t.add_value(2, 'a', 22) #doctest: +ELLIPSIS
    <__init__.TableTimeLimit object at 0x...>
    >>> [map(str, i) for i in t]
    [['11'], ['22']]
    >>> t.add_value(3, 'a', 33) #doctest: +ELLIPSIS
    <__init__.TableTimeLimit object at 0x...>
    >>> [map(str, i) for i in t]
    [['11'], ['22'], ['33']]
    >>> sleep(2)
    >>> [map(str, i) for i in t]
    []
    """

    def __init__(self, timeout, *args, **kwargs):
        Table.__init__(self, *args, **kwargs)
        self._timeout = timeout
        self._cache = {}

    def add_value(self, row, column, value):
        self._cache[row] = time()
        return Table.add_value(self, row, column, value)

    def __iter__(self):
        self._prune_old_rows()
        return Table.__iter__(self)

    def _prune_old_rows(self):
        treshold = time() - self._timeout
        for (key, timestamp) in self._cache.items():
            if timestamp > treshold:
                continue
            del self._rows[key]
            del self._cache[key]
