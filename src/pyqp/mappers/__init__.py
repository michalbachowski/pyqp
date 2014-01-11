#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from functools import wraps

class Keys(object):
    TABLE_NAME = 0
    ROW_ID = 1
    COLUMN_NAME = 2
    VALUE = 3

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
