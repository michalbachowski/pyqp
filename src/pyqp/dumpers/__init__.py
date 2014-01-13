#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain
from functools import wraps
from pyqp.table import Abstract as TableAbstract


def csv_dumper(table):
    """Dumps given table to CSV format

    @param  table -- table to be dumped
    @type   table -- pyqp.table.Abstract

    Usage:
    >>> from pyqp.table import Table
    >>> t = Table('foo', ['column_1', 'column_2'])
    >>> t.add_value(1, 'column_1', 2).add_value(1, 'column_2', 3) #doctest: +ELLIPSIS
    <pyqp.table.Table object at 0x...>
    >>> csv_dumper(t)
    'column_1,column_2\\nstr,str\\n"column_1","column_2"\\n2,3'
    """
    return "\n".join(chain([\
        ','.join([column.name for column in table.columns]),\
        ','.join([column.type_name for column in table.columns]),\
        ','.join(['"%s"' % column.desc for column in table.columns])],\
        [','.join(map(str, row)) for row in table]))


class TableFilterable(TableAbstract):

    def __init__(self, base_table, filter_func):
        self._table = base_table
        self._filter_func = filter_func

    @property
    def name(self):
        return self._table.name

    @property
    def columns(self):
        return self._filter_columns(self._table.columns)

    def __iter__(self):
        return (self._filter_columns(row) for row in iter(self._table))

    def _filter_columns(self, row):
        return (col for col in row if self._filter_func(col.name))


def filterable_dumper(base_dumper, filter_func):

    @wraps(filterable_dumper)
    def _dumper(table):
        return base_dumper(TableFilterable(table, filter_func))
    return _dumper


def decorated_dumper(base_dumper, decorators):
    """Dumps given table using predefined base_dumper.
    Then each of given decorators is applied to received output

    @param  base_dumper -- base dumper to perform table dump
    @type   base_dumper -- callable
    @param  decorators  -- list of decorators to be applied to base_dumper output
    @type   decorators  -- list
    @return type
    """

    def _reduce(data, filter_func):
        return filter_func(data)

    @wraps(decorated_dumper)
    def _dump(table):
        return reduce(_reduce, decorators, base_dumper(table))
    return _dump
