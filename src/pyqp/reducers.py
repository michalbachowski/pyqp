#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import math


# in python there are built in: sum, min and max

def last(values):
    return values[-1]


def nvl(values):
    for val in values:
        if val is not None:
            return val
    raise ValueError('Not None value not found')


class Percentile(object):

    def __init__(self, percentile):
        self._percentile = percentile

    def __call__(self, values):
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
        return sum(values) / len(values)


    def mode(values):
        return max(set(values), key=values.count)
