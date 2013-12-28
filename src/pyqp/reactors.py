#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Abstract(object):

    def dispatch(self, event_name, data):
        pass

    def process(self):
        pass


class Forwarder(Abstract):

    def dispatch(self, event_name, data):
        # TODO forward event to hub
        pass


class Mapper(Abstract):

    def __init__(self):
        self._mappers = {}
        self._tables = {}

    def add_table(self, table):
        if table.name in self._tables:
            raise RuntimeError('Duplicated table')
        self._tables[table.name] = table
        return self

    def add_mapper(self, event_name, mapper):
        if event_name in self._mappers:
            raise RuntimeError('Duplicated mapper')
        self._mappers[event_name] = mapper
        return self

    def dispatch(self, event_name, data):
        for (table, row, column, value) in map(self._mappers[event_name], data):
            self._tables[table].add_value(row, column, value)
        return self

    def process(self):
        pass
