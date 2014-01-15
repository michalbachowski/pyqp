#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain
from functools import wraps

def filtered_configurator(base_configurator, filter_func):

    def _apply_filter(item):
        return filter_func(*item)

    @wraps(filtered_configurator)
    def _configurator(configuration):
        return chain.from_iterable(map(_apply_filter, \
                                            base_configurator(configuration)))
    return _configurator

def simple_dict_config(config):
    yield (config.get('table'), config.get('dumper'), config)

def list_of_configs(base_configurator):
    @wraps(list_of_configs)
    def _configurator(config):
        return chain.from_iterable(map(base_configurator, config))
    return _configurator
