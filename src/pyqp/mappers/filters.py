#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from itertools import chain

def aggregate_filter(*filters):

    def _apply_filters(output, filter_func):
        return chain.from_iterable(map(filter_func, output))

    @wraps(aggregate_filter)
    def _filter(cell):
        return reduce(_apply_filters, filters, [cell])
    return _filter

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

def assign_weight(**weights):
    """Assigns given weights to values for cells from given columns

    >>> aw = assign_weight(foo=2, bar=3)
    >>> [i for i in aw(('table', 'row', 'foo', 1))]
    [('table', 'row', 'foo', (1, 2))]
    >>> [i for i in aw(('table', 'row', 'baz', 1))]
    [('table', 'row', 'baz', 1)]
    """
    def _filter(cell):
        if cell[2] in weights:
            yield _alter_tuple(cell, 3, (cell[3], weights[cell[2]]))
        else:
            yield cell
    return _filter
