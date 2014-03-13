#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain
from functools import wraps
from pyqp.tables.decorators import TableFilterable


def csv_dumper(table):
    """Dumps given table to CSV format

    @param  table -- table to be dumped
    @type   table -- pyqp.table.Abstract

    Usage:
    >>> from pyqp.tables import Table
    >>> from pyqp.column import Column
    >>> t = Table('foo', [Column('column_1'), Column('column_2')])
    >>> t.add_value(1, 'column_1', 2).add_value(1, 'column_2', 3) #doctest: +ELLIPSIS
    <pyqp.tables.Table object at 0x...>
    >>> c = csv_dumper(t)
    >>> c #doctest: +ELLIPSIS
    <generator object csv_dumper at 0x...>
    >>> [i for i in c]
    ['column_1,column_2\\nstr,str\\n"column_1","column_2"\\n2,3']
    """
    yield "\n".join(chain([\
        ','.join([column.name for column in table.columns]),\
        ','.join([column.type_name for column in table.columns]),\
        ','.join(['"%s"' % column.desc for column in table.columns])],\
        [','.join(map(str, row)) for row in table]))


def filtering_table_dumper(base_dumper, col_filter=None, row_filter=None):

    @wraps(filtering_table_dumper)
    def _dumper(table):
        return base_dumper(TableFilterable(table, col_filter, row_filter))
    return _dumper


def filtered_dumper(base_dumper, filter_func):
    """Dumps given table using predefined base_dumper.
    Then given filter is applied to received output

    @param  base_dumper -- base dumper to perform table dump
    @type   base_dumper -- callable
    @param  filter_func -- filter to be applied to base_dumper output
    @type   filter_func -- callable
    @return type
    """

    @wraps(filtered_dumper)
    def _dump(table):
        return chain.from_iterable(map(filter_func, base_dumper(table)))
    return _dump
