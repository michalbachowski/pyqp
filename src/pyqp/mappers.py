#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from functools import wraps

class Keys(object):
    TABLE_NAME = 0
    ROW_ID = 1
    COLUMN_NAME = 2
    VALUE = 3

def _alter_tuple(row, index, value):
    tmp = list(row)
    tmp[index] = value
    return tuple(tmp)

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

def alias(decorated, aliases, key=2):
    @wraps(alias)
    def _map(event_name, iterable):
        for row in decorated(event_name, iterable):
            yield row
            val = row[key]
            if val not in aliases:
                continue
            for alias in aliases[val]:
                yield _alter_tuple(row, key, alias)
    return _map

def select(decorated, allowed, key=2):
    @wraps(select)
    def _map(event_name, iterable):
        for row in decorated(event_name, iterable):
            if row[key] in allowed:
                yield row
    return _map

def exclude(decorated, excluded, key=2):
    @wraps(exclude)
    def _map(event_name, iterable):
        for row in decorated(event_name, iterable):
            if row[key] not in excluded:
                yield row
    return _map
