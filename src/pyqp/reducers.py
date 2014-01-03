#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import math


# in python there are built in: sum, min and max

def last(values):
    """Returns last value from given list

    >>> last([1,2,3])
    3

    >>> last()
    Traceback (most recent call last):
    ...
    TypeError: last() takes exactly 1 argument (0 given)
    """
    return values[-1]


def nvl(values):
    """Returns first non-None value from given list

    >>> nvl([1,2,3])
    1

    >>> nvl([None, 1, None, 2])
    1

    >>> nvl([None])
    Traceback (most recent call last):
    ...
    ValueError: Not None value not found

    >>> nvl()
    Traceback (most recent call last):
    ...
    TypeError: nvl() takes exactly 1 argument (0 given)
    """
    for val in values:
        if val is not None:
            return val
    raise ValueError('Not None value not found')


class Percentile(object):
    """Calculates requested percentile value for given list of values

    >>> Percentile(0.25)([1,2,3,4])
    1.75

    >>> Percentile(0.25)([1,2,3,4,5])
    2

    >>> Percentile(0.5)([1,2,3])
    2

    >>> Percentile(0.5)([1,2,3,4])
    2.5
    """

    def __init__(self, percentile):
        """Object initialization

        >>> Percentile(1)    #doctest: +ELLIPSIS
        <reducers.Percentile object at 0x...>

        >>> Percentile()
        Traceback (most recent call last):
        ...
        TypeError: __init__() takes exactly 2 arguments (1 given)
        """
        self._percentile = percentile

    def __call__(self, values):
        """Find the percentile of a list of values.

        @param    values -- a list of values. Would be sorted internally
        @type     values -- list
        @return   float  -- the percentile of the values

        >>> Percentile(0.25)([1,2,3,4,5])
        2

        >>> Percentile(0.5)([1, 2, 3])
        2

        >>> Percentile(0.75)()
        Traceback (most recent call last):
        ...
        TypeError: __call__() takes exactly 2 arguments (1 given)
        """
        sorts = sorted(values)
        key = (len(values)-1) * self._percentile
        key_floor = math.floor(key)
        key_ceil = math.ceil(key)
        if key_ceil == key_floor:
            return sorts[int(key)]
        d0 = sorts[int(key_floor)] * (key_ceil - key)
        d1 = sorts[int(key_ceil)] * (key - key_floor)
        return d0+d1


# from Python 3.4 "statistics" module is available adding median, mean, mode
# and other statistic functions, see:
# http://docs.python.org/3self.4/library/statistics.html
try:
    from statistics import median, mean, mode
except ImportError:

    median = Percentile(0.5)


    def mean(values):
        """Calculates mean (average) for given numbers

        >>> mean([1,2,3])
        2.0
        >>> mean()
        Traceback (most recent call last):
        ...
        TypeError: mean() takes exactly 1 argument (0 given)
        """
        return sum(values) / len(values)


    def mode(values):
        """Calculates mode (most common value) of given discrete values

        >>> mode([1,1,2,3])
        1

        >>> mode()
        Traceback (most recent call last):
        ...
        TypeError: mode() takes exactly 1 argument (0 given)
        """
        return max(set(values), key=values.count)
