#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial
from .table import TableForwarder


def list_config_reader(iterable):
    for config in iterable:
        yield (None, None, config)


def dict_config_factory(iterable):
    for (table, drawer, config) in iterable:
        yield (config.get('table'), config.get('drawer'), config)


class Filter(object):

    def __call__(self, table, drawer, config):
        raise NotImplementedError()


class AggregateFilter(Filter):

    def __init__(self):
        self._configurators = []

    def __call__(self, iterable):
        for (table, drawer, config) in iterable:
            for configurator in self._configurators:
                (table, drawer, config) = configurator(table, drawer, config)
            yield (table, drawer, config)

    def append(self, configurator):
        self._configurators.append(configurator)
        return self


class MakeTableForwardable(Filter):

    def __init__(self, do_filter, forwarder_factory):
        self._do_filter = do_filter
        self._forwarder_factory = forwarder_factory

    def __call__(self, table, drawer, config):
        if not config.get('aggregate_locally', self._do_filter):
            table = self._forwarder_factory(table.name, table.columns)
        return (table, drawer, config)


class DbusForwardable(MakeTableForwardable):

    def __init__(self, do_filter, dbus):
        MakeTableForwardable.__init__(self, do_filter, \
                                                partial(TableForwarder, dbus))


class SetDefaultDrawer(Filter):

    def __init__(self, drawer):
        self._drawer = drawer

    def __call__(self, table, drawer, config):
        if drawer is None:
            drawer = self._drawer
        return (table, drawer, config)
