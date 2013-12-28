#!/usr/bin/env python
# -*- coding: utf-8 -*-

# in python there are built in: sum, min and max

def last(values):
    for last in values:
        pass
    return last

def avg(values):
    return sum(values) / float(len(values))

def nvl(self, values):
    for val in values:
        if val is not None:
            return val
    raise ValueError('Not None value not found')
