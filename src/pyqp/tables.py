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


class TableTimeLimit(Table):
    """Table that prunes old rows after given amount of seconds.

    >>> from time import sleep
    >>> t = TableTimeLimit(1, 'foo', ['a'])
    >>> t.add_value(1, 'a', 11) #doctest: +ELLIPSIS
    <tables.TableTimeLimit object at 0x...>
    >>> t.add_value(2, 'a', 22) #doctest: +ELLIPSIS
    <tables.TableTimeLimit object at 0x...>
    >>> [map(str, i) for i in t]
    [['11'], ['22']]
    >>> t.add_value(3, 'a', 33) #doctest: +ELLIPSIS
    <tables.TableTimeLimit object at 0x...>
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


class TableForwarder(Abstract):

    def __init__(self, proxy, name, columns):
        self._proxy = proxy
        Abstract.__init__(self, name, columns)

    def add_value(self, row, column, value):
        self._proxy.send('pyqp_cell_value', (self.name, row, column, value))


class TableFilterable(Abstract):
    """Table that filters columns and/or rows from output (it holds all data!)

    >>> from time import sleep
    >>> from operator import attrgetter
    >>> t = Table('foo', ['a', 'b'])
    >>> tf = TableFilterable(t, col_filter=lambda c: c == 'a')
    >>> tf.add_value(1, 'a', 11) #doctest: +ELLIPSIS
    <tables.Table object at 0x...>
    >>> tf.add_value(1, 'b', 22) #doctest: +ELLIPSIS
    <tables.Table object at 0x...>
    >>> map(attrgetter('name'), t.columns)
    ['a', 'b']
    >>> map(attrgetter('name'), tf.columns)
    ['a']
    >>> [map(str, i) for i in t]
    [['11', '22']]
    >>> [map(str, i) for i in tf]
    [['11']]
    """

    def __init__(self, base_table, name=None, col_filter=None, row_filter=None):
        self._table = base_table
        self._name = name
        self._col_filter = col_filter if col_filter is not None else self._true
        self._row_filter = row_filter if row_filter is not None else self._true

    def _true(self, *args, **kwargs):
        """Default filter that will just leave any value"""
        return True

    @property
    def name(self):
        return self._table.name if self._name is None else self._name

    @property
    def columns(self):
        return self._filter_columns(self._table.columns)

    def add_value(self, row, column, value):
        return self._table.add_value(row, column, value)

    def __iter__(self):
        return iter(map(self._filter_columns, self._filter_rows()))

    def _filter_rows(self):
        return filter(self._row_filter, self._table)

    def _filter_columns(self, row):
        return (col for col in row if self._col_filter(col.name))
