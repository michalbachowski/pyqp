#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

def _alter_tuple(row, index, value):
    tmp = list(row)
    tmp[index] = value
    return tuple(tmp)

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
