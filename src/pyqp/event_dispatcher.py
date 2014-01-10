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

    def add_mapper(self, event_name, mapper, filters=[]):
        self._mappers[event_name].append((mapper, filters))
        return self

    def dispatch(self, event_name, data):
        if event_name not in self._mappers:
            return self
        for (table, row, column, value) in self._get_cells(event_name, data):
            self._tables[table].add_value(row, column, value)
        return self

    def _get_cells(self, event_name, data):
        return chain.from_iterable(self._apply_mapper(event_name, mapper, \
                                                                filters, data)
            for (mapper, filters) in self._mappers[event_name])

    def _apply_mapper(self, event_name, mapper, filters, data):
        return chain.from_iterable(reduce(self._filter_cells, filters, [cell]) \
                                        for cell in mapper(event_name, data))

    def _filter_cells(self, iterable, filter_func):
        return chain.from_iterable(map(filter_func, iterable))

    def process(self):
        for table in self._tables.values():
            self._drawers[table.name](table)
