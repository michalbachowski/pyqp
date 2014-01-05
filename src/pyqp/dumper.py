#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from functools import wraps
from itertools import chain


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


def prefix_dumper(base_dumper, prefix):
    """Dumper that prepends output from base_dumper with given prefix.
    Output and prefix are separated with newline character.

    @param  base_dumper -- base dumper that dumps table
    @type   base_dumper -- callable
    @param  prefix      -- string to prepend dumped data with
    @type   prefix      -- string
    @return callable    -- callable - when called with table to be dumped - returns string

    Usage:

    >>> prefix_dumper(lambda x: x, 'foo')('bar')
    'foo\\nbar'
    >>> prefix_dumper(None, 'foo')('bar')
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not callable
    """
    p = str(prefix)
    @wraps(prefix_dumper)
    def _dumper(table):
        return p + "\n" + base_dumper(table)
    return _dumper


def file_dumper(base_dumper, file_name):
    """Writes data received from base_dumper to given file.
    Creates file if necessary

    @param  base_dumper -- base dumper that dumps table
    @type   base_dumper -- callable
    @param  file_name   -- file where to write data
    @type   file_name   -- string
    @return callable    -- callable - when called with table to be dumped - returns string

    Usage:
    >>> import os.path
    >>> import os
    >>> file_dumper(lambda x: x, '/tmp/test')('foo')
    'foo'
    >>> os.path.exists('/tmp/test')
    True
    >>> with open('/tmp/test') as f:
    ...     print f.read()
    foo
    >>> os.unlink('/tmp/test')
    """
    @wraps(file_dumper)
    def _dumper(table):
        with open(file_name, 'w') as f:
            data = base_dumper(table)
            f.write(data)
        return data
    return _dumper


def stdout_dumper(base_dumper):
    """Writes data received from base_dumper to STDOUT

    @param  base_dumper -- base dumper that dumps table
    @type   base_dumper -- callable
    @return callable    -- callable - when called with table to be dumped - returns string

    Usage:
    >>> a=stdout_dumper(lambda x: x)('foo')
    foo
    >>> a
    'foo'
    >>> stdout_dumper(None)('bar')
    Traceback (most recent call last):
    ...
    TypeError: 'NoneType' object is not callable
    """
    @wraps(stdout_dumper)
    def _dumper(table):
        data = base_dumper(table)
        sys.stdout.write(data)
        return data
    return _dumper
