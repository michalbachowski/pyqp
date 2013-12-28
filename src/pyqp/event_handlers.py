#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain
from collections import defaultdict


class Abstract(object):

    def dispatch(self, event_name, data):
        pass

    def process(self):
        pass


class Aggregate(Abstract):

    def __init__(self):
        self._handlers = []

    def append(self, handler):
        self._handlers.append(handler)
        return self

    def dispatch(self, event_name, data):
        for handler in self._handlers:
            handler.dispatch(event_name, data)
        return self

    def process(self):
        for handler in self._handlers:
            handler.process()
        return self


class Forward(Abstract):

    def dispatch(self, event_name, data):
        # TODO forward event to hub
        pass


class Process(Abstract):

    def __init__(self):
        self._mappers = defaultdict(list)
        self._tables = {}
        self._drawers = {}

    def add_table(self, table, drawer):
        if table.name in self._tables:
            raise RuntimeError('Duplicated table')
        self._tables[table.name] = table
        self._drawers[table.name] = drawer
        return self

    def add_mapper(self, event_name, mapper):
        if event_name in self._mappers:
            raise RuntimeError('Duplicated mapper')
        self._mappers[event_name].append(mapper)
        return self

    def dispatch(self, event_name, data):
        if event_name not in self._mappers:
            return self
        for (table, row, column, value) in self._map_data(event_name, data):
            self._tables[table].add_value(row, column, value)
        return self

    def _map_data(self, event_name, data):
        return chain.from_iterable(mapper(data) \
                                        for mapper in self._mappers[event_name])

    def process(self):
        for table in self._tables.values():
            print self._drawers[table.name](table)
