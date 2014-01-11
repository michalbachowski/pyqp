#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain
from functools import wraps


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
        [','.join(map(str, row.values())) for row in table]))


def filterable_dumper(base_dumper, filters):
    """Dumps given table using predefined base_dumper.
    Then each of given filters is applied to received output

    @param  base_dumper -- base dumper to perform table dump
    @type   base_dumper -- callable
    @param  filters     -- list of filters to be applied to base_dumper output
    @type   filters     -- list
    @return type
    """

    def _reduce(data, filter_func):
        return filter_func(data)

    @wraps(filterable_dumper)
    def _dump(table):
        return reduce(_reduce, filters, base_dumper(table))
    return _dump
