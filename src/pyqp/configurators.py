#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial, wraps
from pyqp.table import TableForwarder


def list_of_dicts_to_list_of_tuples(iterable):
    for config in iterable:
        yield (None, None, config)


def simple_dict_factory(table, drawer, config):
    return (config.get('table'), config.get('drawer'), config)


def aggregate_filter(*filters):
    @wraps(aggregate_filter)
    def _filter(table, drawer, config):
        for f in filters:
            (table, drawer, config) = f(table, drawer, config)
        return (table, drawer, config)
    return _filter


def make_table_forwardable(allow_forwarding, forwarder_factory):
    @wraps(make_table_forwardable)
    def _filter(table, drawer, config):
        if not config.get('aggregate_locally', allow_forwarding):
            table = forwarder_factory(table.name, table.columns)
        return (table, drawer, config)
    return _filter


def dbus_forwardable(allow_forwarding, dbus):
    return make_table_forwardable(allow_forwarding, \
                                                partial(TableForwarder, dbus))


def set_default_drawer(drawer):
    @wraps(set_default_drawer)
    def _filter(table, _drawer, config):
        if _drawer is None:
            _drawer = drawer
        return (table, _drawer, config)
    return _filter
