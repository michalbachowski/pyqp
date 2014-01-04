#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from functools import wraps


def dict_row(table, primary_key_columns):
    _pk = itemgetter(*primary_key_columns)
    @wraps(dict_row)
    def _map(data):
        pk = _pk(data)
        for (column, value) in data.items():
            yield (table, pk, column, value)
    return _map


def single_value(data):
    yield (data[0], data[1], data[2], data[3])


def values_list(data):
    for value in data:
        yield (value[0], value[1], value[2], value[3])


def alias(decorated, aliases):
    @wraps(alias)
    def _map(iterable):
        for row in decorated(iterable):
            yield row
            if row[2] not in aliases:
                return
            for alias in aliases[row[2]]:
                yield (row[0], row[1], alias, row[3])
    return _map


def select(decorated, allowed):
    @wraps(select)
    def _map(iterable):
        for row in decorated(iterable):
            if row[2] in allowed:
                yield row
    return _map


def exclude(decorated, excluded):
    @wraps(exclude)
    def _map(iterable):
        for row in decorated(iterable):
            if row[2] not in excluded:
                yield row
    return _map
