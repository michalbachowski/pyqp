#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain
from collections import defaultdict


class Dispatcher(object):

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
            self._drawers[table.name](table)
