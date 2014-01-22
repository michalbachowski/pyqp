#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from functools import wraps
from itertools import chain


class Keys(object):
    TABLE_NAME = 0
    ROW_ID = 1
    COLUMN_NAME = 2
    VALUE = 3

def filtered_mapper(base_mapper, filter_func):
    """First filters given data using predefined base_mapper,
    then given filter is applied to received output

    @param  base_mapper -- base mapper to perform table map
    @type   base_mapper -- callable
    @param  filter_func -- filter to be applied to base_mapper output
    @type   filter_func -- callable
    @return callable -- callable that accepts one argument: input data

    >>> m = filtered_mapper(lambda e, x: [x], lambda x: [x+1])
    >>> list(m('event_name', 2))
    [3]
    """

    @wraps(filtered_mapper)
    def _map(event_name, data):
        return chain.from_iterable(map(filter_func, base_mapper(event_name, \
                                                                        data)))
    return _map

def dict_row(*primary_key_columns):
    """Maps table data given as dict to list of tuples
    [(table_name, pk, column, value), ...]
    Event name is treated as table name and primary key is composed
    from values from one or more columns.

    @param  *primary_key_columns -- one or more columns names that composes primary key
    @type   *primary_key_columns -- str
    @return type

    >>> from operator import itemgetter
    >>> m = dict_row('a')
    >>> ig = itemgetter(2)
    >>> sorted(list(m('event_name', {'a': 1, 'b': 3})), key=ig) == sorted([('event_name', 1, 'a', 1), ('event_name', 1, 'b', 3)], key=ig)
    True
    """
    _pk = itemgetter(*primary_key_columns)
    @wraps(dict_row)
    def _map(event_name, data):
        pk = _pk(data)
        for (column, value) in data.items():
            yield (event_name, pk, column, value)
    return _map

def single_value(event_name, data):
    """Mapper that accepts single tuple with data

    @param  event_name -- name of event
    @type   event_name -- str
    @param  data       -- iterable: (table_name, pk, column, value)
    @param  data       -- iterable
    @return iterable

    VALUES ARE PASSED BY REFERNCE

    >>> list(single_value('foo', [1, 2, 3, 4]))
    [(1, 2, 3, 4)]
    >>> list(single_value('foo', [1, 2, 3, 4, 5, 6]))
    [(1, 2, 3, 4)]
    """
    yield (data[0], data[1], data[2], data[3])

def values_list(event_name, data):
    """Mapper that accepts iterable with iterables with data

    @param  event_name -- name of event
    @type   event_name -- str
    @param  data       -- iterable of iterables: [(table_name, pk, column, value)]
    @param  data       -- iterable
    @return iterable

    VALUES ARE PASSED BY REFERNCE

    >>> list(values_list('foo', [[1, 2, 3, 4]]))
    [(1, 2, 3, 4)]
    >>> list(values_list('foo', [[1, 2, 3, 4, 5, 6]]))
    [(1, 2, 3, 4)]
    """
    return chain.from_iterable([single_value(event_name, v) for v in data])
