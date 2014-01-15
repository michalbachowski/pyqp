#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain, imap, cycle
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
        self._mappers[event_name].append(mapper)
        return self

    def dispatch(self, event_name, data):
        for (table, row, column, value) in self._get_cells(event_name, data):
            self._tables[table].add_value(row, column, value)
        return self

    def _get_cells(self, event_name, data):
        return chain.from_iterable(imap(self._map_event_data, \
                cycle([event_name]), self._mappers[event_name], cycle([data])))

    def _map_event_data(self, event_name, mapper, data):
        return mapper(event_name, data)

    def process(self):
        for table in self._tables.values():
            # execute lazy evaluation (generators)
            [i for i in self._drawers[table.name](table)]
