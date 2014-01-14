#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import copy
from functools import wraps
from pyqp.columns import Column


def aggregate_factory(*factories):
    @wraps(aggregate_factory)
    def _factory(config):
        for factory in factories:
            try:
                return factory(config)
            except TypeError:
                pass
        raise ValueError("Expected valid column configuration, got %s" % config)
    return _factory

def column_instance_factory(config):
    # so maybe config is valid Column instance?
    try:
        config.name
        config.desc
        config.type_name
        config.append
        config.reduce
        config.__copy__
        config.__str__
    except AttributeError:
        raise TypeError('Expected config to be instance of "Column", got %s' % \
                                                                type(config))
    else:
        return copy(config)

def dict_factory(config):
    try:
        return Column(**config)
    except TypeError:
        raise TypeError('Expected config to a dict, got %s' % type(config))

def tuple_factory(config):
    try:
        return Column(*config)
    except TypeError:
        raise TypeError('Expected config to a tuple, got %s' % type(config))

def string_factory(config):
    try:
        return Column(config)
    except TypeError:
        raise TypeError('Expected config to a string, got %s' % type(config))


default_column_factory = aggregate_factory(column_instance_factory, \
                                    dict_factory, tuple_factory, string_factory)
