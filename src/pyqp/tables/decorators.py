#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Abstract(object):

    def __init__(self, base_table, *args, **kwargs):
        self._table = base_table

    @property
    def name(self):
        return self._table.name

    @property
    def columns(self):
        return self._table.columns

    def add_value(self, row, column, value):
        return self._table.add_value(row, column, value)

    def __iter__(self):
        return iter(self._table)


class TableForwarder(Abstract):

    def __init__(self, base_table, allow_forwarding, proxy):
        self._proxy = proxy
        self._do_forward = allow_forwarding
        Abstract.__init__(self, base_table)

    def add_value(self, row, column, value):
        if self._do_forward(self.name):
            self._proxy.send('pyqp_cell_value', (self.name, row, column, value))
        else:
            Abstract.add_value(self, row, column, value)
        return self


class TableFilterable(Abstract):
    """Table that filters columns and/or rows from output (it holds all data!)

    >>> from time import sleep
    >>> from operator import attrgetter
    >>> from pyqp.tables import Table
    >>> t = Table('foo', ['a', 'b'])
    >>> tf = TableFilterable(t, col_filter=lambda c: c == 'a')
    >>> tf.add_value(1, 'a', 11) #doctest: +ELLIPSIS
    <pyqp.tables.Table object at 0x...>
    >>> tf.add_value(1, 'b', 22) #doctest: +ELLIPSIS
    <pyqp.tables.Table object at 0x...>
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
        Abstract.__init__(self, base_table)
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

    def __iter__(self):
        return iter(map(self._filter_columns, self._filter_rows()))

    def _filter_rows(self):
        return filter(self._row_filter, self._table)

    def _filter_columns(self, row):
        return (col for col in row if self._col_filter(col.name))
