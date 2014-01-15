#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain
from functools import wraps

def filtered_configurator(base_configurator, filter_func):

    def _apply_filter(item):
        return filter_func(*item)

    @wraps(filtered_configurator)
    def _configurator(configuration):
        return chain.from_iterable(map(_apply_filter, map(base_configurator, \
                                                                configuration)))
    return _configurator

def simple_dict_factory(config):
    return (config.get('table'), config.get('dumper'), config)
