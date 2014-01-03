#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from pyqp.table import TableForwarder


def list_of_dicts_to_list_of_tuples(iterable):
    for config in iterable:
        yield (None, None, config)


def simple_dict_factory(table, drawer, config):
    return (config.get('table'), config.get('drawer'), config)


class Filter(object):

    def __call__(self, table, drawer, config):
        return (table, drawer, config)


class AggregateFilter(Filter):

    def __init__(self):
        self._filters = []

    def __call__(self, table, drawer, config):
        for filter in self._filters:
            (table, drawer, config) = filter(table, drawer, config)
        return (table, drawer, config)

    def append(self, filter):
        self._filters.append(filter)
        return self


class MakeTableForwardable(Filter):

    def __init__(self, allow_forwarding, forwarder_factory):
        self._allow_forwarding = allow_forwarding
        self._forwarder_factory = forwarder_factory

    def __call__(self, table, drawer, config):
        if self._is_forwardable(config):
            table = self._forwarder_factory(table.name, table.columns)
        return (table, drawer, config)

    def _is_forwardable(self, config):
        return not config.get('aggregate_locally', self._allow_forwarding)


class DbusForwardable(MakeTableForwardable):

    def __init__(self, allow_forwarding, dbus):
        MakeTableForwardable.__init__(self, allow_forwarding, \
                                                partial(TableForwarder, dbus))


class SetDefaultDrawer(Filter):

    def __init__(self, drawer):
        self._drawer = drawer

    def __call__(self, table, drawer, config):
        if drawer is None:
            drawer = self._drawer
        return (table, drawer, config)
