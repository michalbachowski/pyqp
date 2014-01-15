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
    """Creates new instance out of existing Column instance

    >>> c = Column('foo')
    >>> c1 = column_instance_factory(c)
    >>> c == c1
    False
    >>> c1.name == c.name
    True
    >>> column_instance_factory('f')
    Traceback (most recent call last):
    ...
    TypeError: Expected config to be instance of pyqp.columns.Column, got <type 'str'>
    """
    try:
        config.name
        config.desc
        config.type_name
        config.append
        config.reduce
        config.__copy__
        config.__str__
    except AttributeError:
        raise TypeError('Expected config to be instance of pyqp.columns.Column, got %s' % \
                                                                type(config))
    else:
        return copy(config)

def dict_factory(config):
    """Creates new instance of Column using given dict

    >>> c = dict_factory({'name': 'ggg'})
    >>> c.name
    'ggg'
    >>> dict_factory('f')
    Traceback (most recent call last):
    ...
    TypeError: Expected config to be a dict, got <type 'str'>
    """
    try:
        return Column(**config)
    except TypeError:
        raise TypeError('Expected config to be a dict, got %s' % type(config))

def tuple_factory(config):
    """Creates new instance of Column using given tuple / list

    >>> c = tuple_factory(('ggg',))
    >>> c.name
    'ggg'
    >>> tuple_factory('f')
    Traceback (most recent call last):
    ...
    TypeError: Expected config to be a tuple, got <type 'str'>
    """
    try:
        # ensure we work with iterable (list or tuple), not str
        config.__iter__
        return Column(*config)
    except (TypeError, AttributeError):
        raise TypeError('Expected config to be a tuple, got %s' % type(config))

def string_factory(config):
    """Creates new instance of Column using given string

    >>> c = string_factory('ggg')
    >>> c.name
    'ggg'
    >>> string_factory(['123'])
    Traceback (most recent call last):
    ...
    TypeError: Expected config to be a string, got <type 'list'>
    """
    try:
        # ensure we work with str
        config.strip
        return Column(config)
    except (TypeError, AttributeError):
        raise TypeError('Expected config to be a string, got %s' % type(config))


default_column_factory = aggregate_factory(column_instance_factory, \
                                    dict_factory, tuple_factory, string_factory)