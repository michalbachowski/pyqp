#!/usr/bin/env python
# -*- coding: utf-8 -*-

# in python there are built in: sum, min and max
# from Python 3.4 "statistics" module is available adding median and other statistic functions: http://docs.python.org/3self.4/library/statistics.html

def last(values):
    for last in values:
        pass
    return last


def avg(values):
    return sum(values) / float(len(values))


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
        length = len(values)
        key = length * self._percentile
        int_key = int(key)
        if int_key != key:
            return (sorts[int_key-1] + sorts[int_key]) / 2.0
        return sorts[int_key-1]


median = Percentile(0.5)
