#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain, cycle
from collections import defaultdict
from six.moves import map


class Manager(object):

    def __init__(self):
        self._mappers = defaultdict(list)
        self._tables = {}
        self._dumpers = {}

    def add_table(self, table, dumper):
        if table.name in self._tables:
            raise ValueError("duplicate table '{0}' found".format(table.name))
        self._tables[table.name] = table
        self._dumpers[table.name] = dumper
        return self

    def add_mapper(self, event_name, mapper):
        self._mappers[event_name].append(mapper)
        return self

    def dispatch(self, event_name, data):
        for (table, row, column, value) in self._get_cells(event_name, data):
            self._tables[table].add_value(row, column, value)
        return self

    def _get_cells(self, event_name, data):
        return chain.from_iterable(map(self._map_event_data, \
                cycle([event_name]), self._mappers[event_name], cycle([data])))

    def _map_event_data(self, event_name, mapper, data):
        return mapper(event_name, data)

    def dump(self):
        for table in self._tables.values():
            # execute lazy evaluation (generators)
            [i for i in self._dumpers[table.name](table)]
