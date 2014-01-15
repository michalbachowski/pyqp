#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial, wraps
from pyqp.tables.decorators import TableForwarder


def list_of_dicts_to_list_of_tuples(iterable):
    for config in iterable:
        yield (None, None, config)


def simple_dict_factory(table, dumper, config):
    return (config.get('table'), config.get('dumper'), config)


def aggregate_filter(*filters):
    @wraps(aggregate_filter)
    def _filter(table, dumper, config):
        for f in filters:
            (table, dumper, config) = f(table, dumper, config)
        return (table, dumper, config)
    return _filter


def decorate_table(allow_decorating, decorator):
    @wraps(decorate_table)
    def _filter(table, dumper, config):
        if allow_decorating(config):
            table = decorator(table)
        return (table, dumper, config)
    return _filter


def make_forwardable(allow_forwarding, proxy):
    return decorate_table(lambda c: True, partial(TableForwarder, proxy=proxy, \
                                            allow_forwarding=allow_forwarding))


def set_default_dumper(dumper):
    @wraps(set_default_dumper)
    def _filter(table, _dumper, config):
        if _dumper is None:
            _dumper = dumper
        return (table, _dumper, config)
    return _filter
