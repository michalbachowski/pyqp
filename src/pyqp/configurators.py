#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial, wraps
from pyqp.table import TableForwarder


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


def make_table_forwardable(allow_forwarding, forwarder_factory):
    @wraps(make_table_forwardable)
    def _filter(table, dumper, config):
        if not config.get('aggregate_locally', allow_forwarding):
            table = forwarder_factory(table.name, table.columns)
        return (table, dumper, config)
    return _filter


def dbus_forwardable(allow_forwarding, dbus):
    return make_table_forwardable(allow_forwarding, \
                                                partial(TableForwarder, dbus))


def set_default_dumper(dumper):
    @wraps(set_default_dumper)
    def _filter(table, _dumper, config):
        if _dumper is None:
            _dumper = dumper
        return (table, _dumper, config)
    return _filter
