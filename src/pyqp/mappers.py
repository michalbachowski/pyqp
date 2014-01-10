#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from functools import wraps


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


def alias(decorated, aliases):
    @wraps(alias)
    def _map(event_name, iterable):
        for row in decorated(event_name, iterable):
            yield row
            if row[2] not in aliases:
                continue
            for alias in aliases[row[2]]:
                yield (row[0], row[1], alias, row[3])
    return _map


def select(decorated, allowed):
    @wraps(select)
    def _map(event_name, iterable):
        for row in decorated(event_name, iterable):
            if row[2] in allowed:
                yield row
    return _map


def exclude(decorated, excluded):
    @wraps(exclude)
    def _map(event_name, iterable):
        for row in decorated(event_name, iterable):
            if row[2] not in excluded:
                yield row
    return _map
