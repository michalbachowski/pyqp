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
    """Dumps given table using predefined base_mapper.
    Then given filter is applied to received output

    @param  base_mapper -- base mapper to perform table map
    @type   base_mapper -- callable
    @param  filter_func -- filter to be applied to base_mapper output
    @type   filter_func -- callable
    @return type
    """

    @wraps(filtered_mapper)
    def _map(event_name, data):
        return chain.from_iterable(map(filter_func, base_mapper(event_name, \
                                                                        data)))
    return _map

def dict_row(primary_key_columns):
    _pk = itemgetter(*primary_key_columns)
    @wraps(dict_row)
    def _map(event_name, data):
        pk = _pk(data)
        for (column, value) in data.items():
            yield (event_name, pk, column, value)
    return _map

def single_value(event_name, data):
    yield (data[0], data[1], data[2], data[3])

def values_list(event_name, data):
    for value in data:
        yield (value[0], value[1], value[2], value[3])
