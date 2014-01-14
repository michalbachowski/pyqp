#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from functools import wraps
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


def percentile(percent):
    """Find the percentile of a list of values.

    >>> percentile(1)    #doctest: +ELLIPSIS
    <function percentile at 0x...>

    >>> percentile()
    Traceback (most recent call last):
    ...
    TypeError: percentile() takes exactly 1 argument (0 given)

    >>> percentile(0.25)([1,2,3,4])
    1.75

    >>> percentile(0.25)([1,2,3,4,5])
    2

    >>> percentile(0.5)([1,2,3])
    2

    >>> percentile(0.5)([1,2,3,4])
    2.5
    """
    @wraps(percentile)
    def _reduce(iterable):
        sorts = sorted(iterable)
        key = (len(iterable)-1) * percent
        key_floor = math.floor(key)
        key_ceil = math.ceil(key)
        if key_ceil == key_floor:
            return sorts[int(key)]
        d0 = sorts[int(key_floor)] * (key_ceil - key)
        d1 = sorts[int(key_ceil)] * (key - key_floor)
        return d0+d1
    return _reduce


def weighted_average(iterable):
    """
    Takes a list of tuples (value, weight) and
    returns weighted average as calculated by
    Sum of all values * weights / Sum of all weights

    >>> weighted_average([1,2,3])
    Traceback (most recent call last):
    ...
    TypeError: 'int' object is not iterable
    >>> weighted_average([(1, 1), (2, 1)])
    1.5
    >>> weighted_average([(1, 3), (3, 3)])
    2.0
    """
    numerator = 0
    denominator = 0
    for (value, weight) in iterable:
        denominator += weight
        numerator += value * weight
    return numerator / denominator


# from Python 3.4 "statistics" module is available adding median, mean, mode
# and other statistic functions, see:
# http://docs.python.org/3self.4/library/statistics.html
try:
    from statistics import median, mean, mode
except ImportError:

    median = percentile(0.5)


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
