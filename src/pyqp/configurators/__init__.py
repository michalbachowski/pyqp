#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain
from functools import wraps

def filtered_configurator(base_configurator, filter_func):
    """Factory method that creates configuration and applies given filter to received output

    >>> f = filtered_configurator(lambda c: [(1, 2, 3)], lambda a, b, c: [(a+10, b+10, c+10)])
    >>> f # doctest: +ELLIPSIS
    <function filtered_configurator at 0x...>
    >>> list(f('fooo'))
    [(11, 12, 13)]
    """

    def _apply_filter(item):
        return filter_func(*item)

    @wraps(filtered_configurator)
    def _configurator(configuration):
        return chain.from_iterable(map(_apply_filter, \
                                            base_configurator(configuration)))
    return _configurator

def simple_dict_config(config):
    """Factory method that creates configuration for table from given dictionary

    >>> list(simple_dict_config({'table': 'foo', 'dumper': 'bar'}))
    [('foo', 'bar', {'table': 'foo', 'dumper': 'bar'})]
    >>> list(simple_dict_config({}))
    [(None, None, {})]
    """
    yield (config.get('table'), config.get('dumper'), config)

def list_of_configs(base_configurator):
    """Factory method that creates configuration for table from given list of configurations

    >>> f = list_of_configs(simple_dict_config)
    >>> f # doctest: +ELLIPSIS
    <function list_of_configs at 0x...>
    >>> list(f([{'table': 'foo', 'dumper': 'bar'}]))
    [('foo', 'bar', {'table': 'foo', 'dumper': 'bar'})]
    """
    @wraps(list_of_configs)
    def _configurator(config):
        return chain.from_iterable(map(base_configurator, config))
    return _configurator
