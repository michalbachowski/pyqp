#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from functools import wraps
from itertools import chain


def aggregate_filter(*filters):

    def _apply_filters(output, filter_func):
        return chain.from_iterable(map(filter_func, output))

    @wraps(aggregate_filter)
    def _filter(data):
        return reduce(_apply_filters, filters, [data])
    return _filter


def prepend(prefix):
    """Prepends given string with predefined prefix.
    Output and prefix are separated with newline character.

    @param  prefix      -- string to prepend dumped data with
    @type   prefix      -- string
    @return callable    -- callable - when called with string data - returns string

    Usage:

    >>> prepend('foo')('bar')
    'foo\\nbar'
    """
    p = str(prefix)
    @wraps(prepend)
    def _decorator(data):
        yield p + "\n" + data
    return _decorator


def write_to_file(file_name):
    """Writes received data to given file.
    Creates file if necessary

    @param  file_name   -- file where to write data
    @type   file_name   -- string
    @return callable    -- callable - when called with string data - returns string

    Usage:
    >>> import os.path
    >>> import os
    >>> write_to_file('/tmp/test')('foo')
    'foo'
    >>> os.path.exists('/tmp/test')
    True
    >>> with open('/tmp/test') as f:
    ...     print f.read()
    foo
    >>> os.unlink('/tmp/test')
    """
    @wraps(write_to_file)
    def _decorator(data):
        with open(file_name, 'w') as f:
            f.write(data)
        yield data
    return _decorator


def write_to_stdout(data):
    """Writes received data to STDOUT and returns given data so another
    decorator can use it

    Usage:
    >>> a=write_to_stdout('foo')
    foo
    >>> a
    'foo'
    """
    sys.stdout.write(data)
    yield data
