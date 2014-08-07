#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
from pyqp.column import Column


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
    >>> column_instance_factory('f') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: Expected config to be instance of pyqp.column.Column, got <... 'str'>
    """
    try:
        config.name
        config.desc
        config.type_name
        config.append
        config.reduce
        config.__str__
        return config.duplicate()
    except AttributeError:
        raise TypeError('Expected config to be instance of pyqp.column.Column, got %s' % \
                                                                type(config))

def callable_factory(config):
    """Creates new instance using given callable (usually partial)

    >>> from functools import partial
    >>> p = partial(Column, 'foo')
    >>> c = callable_factory(p)
    >>> c.name
    'foo'
    >>> callable_factory('f') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: Expected config to be callable, got <... 'str'>
    """
    try:
        return config()
    except TypeError:
        raise TypeError('Expected config to be callable, got %s' % type(config))

def dict_factory(config):
    """Creates new instance of Column using given dict

    >>> c = dict_factory({'name': 'ggg'})
    >>> c.name
    'ggg'
    >>> dict_factory('f') # doctest: +IGNORE_EXCEPTION_DETAIL, +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError...
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
    >>> tuple_factory('f') # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: Expected config to be a tuple, got <... 'str'>
    """
    try:
        # ensure we work with iterable (list or tuple), not str
        config.__iter__
        if not hasattr(config, 'strip'):
            return Column(*config)
    except (TypeError, AttributeError):
        pass
    raise TypeError('Expected config to be a tuple, got %s' % type(config))

def string_factory(config):
    """Creates new instance of Column using given string

    >>> c = string_factory('ggg')
    >>> c.name
    'ggg'
    >>> string_factory(['123']) # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: Expected config to be a string, got <... 'list'>
    """
    try:
        # ensure we work with str
        config.strip
        return Column(config)
    except (AttributeError, TypeError):
        raise TypeError('Expected config to be a string, got %s' % type(config))

default_column_factory = lambda *args: list(map(\
            aggregate_factory(column_instance_factory, callable_factory, \
                    dict_factory, tuple_factory, string_factory), \
            args))
