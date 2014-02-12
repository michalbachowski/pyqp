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

    def remove_row(self, key):
        self._table.remove_row(key)
        return self


    def __iter__(self):
        return iter(self._table)


class TableForwarder(Abstract):
    """Table decorator that allow forwarding values using predefined proxy.
    Decision whether to forward or not is made using given callable.

    @param   base_table -- table to decorate
    @type    base_table -- pyqp.tables.Table
    @param   allow_forwarding -- callable that tells whether forwarding is allowed or not
    @type    allow_forwarding -- callable
    @param   sender -- callable that is responsible for forwarding
    @type    sender -- callable
    @returns self -- TableForwarder

    >>> from pyqp.tables import Table
    >>> from sys import stdout
    >>> t = Table('foo', ['a'])
    >>> allow = False
    >>> fwd = lambda table_name: allow
    >>> sender = lambda event_name, cell: stdout.write((event_name, cell))
    >>> tf = TableForwarder(t, fwd, sender)
    >>> tf.add_value(1, 'a', 11) #doctest: +ELLIPSIS
    <decorators.TableForwarder object at 0x...>
    >>> [map(str, i) for i in t]
    [['11']]
    >>> allow = True
    >>> x = tf.add_value(2, 'a', 12)
    ('pyqp_cell_value', ('foo', 2, 'a', 12))
    >>> [map(str, i) for i in t]
    [['11']]
    """
    def __init__(self, base_table, allow_forwarding, sender):
        self._sender = sender
        self._do_forward = allow_forwarding
        Abstract.__init__(self, base_table)

    def add_value(self, row, column, value):
        if self._do_forward(self.name):
            self._sender('pyqp_cell_value', (self.name, row, column, value))
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
