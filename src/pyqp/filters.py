#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

def _alter_tuple(cell, index, value):
    tmp = list(cell)
    tmp[index] = value
    return tuple(tmp)

def alias(*args, **aliases):
    try:
        key = args[0]
    except IndexError:
        key = 2
    @wraps(alias)
    def _filter(cell):
        yield cell
        val = cell[key]
        if val not in aliases:
            return
        for alias in aliases[val]:
            yield _alter_tuple(cell, key, alias)
    return _filter

def select(*allowed, **kwargs):
    key = kwargs.get('key', 2)
    @wraps(select)
    def _filter(cell):
        if cell[key] in allowed:
            yield cell
    return _filter

def exclude(*excluded, **kwargs):
    key = kwargs.get('key', 2)
    @wraps(exclude)
    def _filter(cell):
        if cell[key] not in excluded:
            yield cell
    return _filter
