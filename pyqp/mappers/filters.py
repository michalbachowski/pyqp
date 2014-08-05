#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from itertools import chain
from copy import deepcopy

def aggregate_filter(*filters):
    """Filter that aggregates other filters and uses them to filter value

    >>> f = aggregate_filter(lambda x: [x*2])
    >>> list(f(2))
    [4]
    >>> f = aggregate_filter(lambda x: [x, x*2], lambda x: [x+10, x+20])
    >>> list(f(2))
    [12, 22, 14, 24]
    """

    def _apply_filters(output, filter_func):
        return chain.from_iterable(map(filter_func, output))

    @wraps(aggregate_filter)
    def _filter(cell):
        return reduce(_apply_filters, filters, [cell])
    return _filter

def _alter_tuple(cell, index, value):
    """Alters given tuple: changes value from given index to given new value.
    It casts tuple to list, puts new value and returns tuple"""
    tmp = list(cell)
    tmp[index] = value
    return tuple(tmp)

def alias(*args, **aliases):
    """Filter returns all given tuples plus copies of those
    having value under given key (table name, pk, column name or value)
    found in alias list. You may put as many aliases as you want.

    VALUES ARE PASSED AS REFERENCE!

    >>> f = alias(a=['b'])
    >>> list(f((1, 2, 3, 4)))
    [(1, 2, 3, 4)]
    >>> list(f((1, 2, 'a', 4)))
    [(1, 2, 'a', 4), (1, 2, 'b', 4)]
    >>> f= alias(1, a=['b'])
    >>> list(f((1, 2, 3, 4)))
    [(1, 2, 3, 4)]
    >>> list(f((1, 2, 'a', 4)))
    [(1, 2, 'a', 4)]
    >>> list(f((1, 'a', 3, 4)))
    [(1, 'a', 3, 4), (1, 'b', 3, 4)]
    """
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
    """Filter returns only tuples having value under given key
    (table name, pk, column name or value) allowed.


    >>> f = select('a', 'b')
    >>> list(f((1, 2, 3, 4)))
    []
    >>> list(f((1, 2, 'a', 4)))
    [(1, 2, 'a', 4)]
    >>> f= select('a', 'b', key=1)
    >>> list(f((1, 2, 3, 4)))
    []
    >>> list(f((1, 2, 'a', 4)))
    []
    >>> list(f((1, 'a', 3, 4)))
    [(1, 'a', 3, 4)]
    """

    key = kwargs.get('key', 2)
    @wraps(select)
    def _filter(cell):
        if cell[key] in allowed:
            yield cell
    return _filter

def exclude(*excluded, **kwargs):
    """Filter returns all tuples except those having value under given key
    (table name, pk, column name or value) disallowed.


    >>> f = exclude('a', 'b')
    >>> list(f((1, 2, 3, 4)))
    [(1, 2, 3, 4)]
    >>> list(f((1, 2, 'a', 4)))
    []
    >>> f= exclude('a', 'b', key=1)
    >>> list(f((1, 2, 3, 4)))
    [(1, 2, 3, 4)]
    >>> list(f((1, 2, 'a', 4)))
    [(1, 2, 'a', 4)]
    >>> list(f((1, 'a', 3, 4)))
    []
    """
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

def dereference(key=3):
    """Dereferences value from given key (makes deepcopy of it)

    >>> f = dereference()
    >>> v = (1, 2, 3, ['a', 'b'])
    >>> w = list(f(v))[0]
    >>> w == v
    True
    >>> [w[i] == v[i] for i in range(4)]
    [True, True, True, True]
    >>> [id(w[i]) == id(v[i]) for i in range(4)]
    [True, True, True, False]
    """
    @wraps(dereference)
    def _filter(cell):
        yield _alter_tuple(cell, key, deepcopy(cell[key]))
    return _filter
