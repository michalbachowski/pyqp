#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Direct(object):

    def __init__(self, table, pk):
        self._table = table
        self._pk = frozenset(pk)

    def __call__(self, data):
        pk = self._compute_pk(data)
        for (column, value) in data.items():
            yield (self._table, pk, column, value)

    def _compute_pk(self, data):
        pk = []
        for column in self._pk:
            pk.append(data[column])
        return frozenset(pk) # to make it hashable


class Alias(object):

    def __init__(self, decorated, aliases):
        self._decorated = decorated
        self._aliases = aliases

    def __call__(self, data):
        for row in self._decorated(data):
            yield row
            if row[1] not in self._aliases:
                continue
            for alias in self._aliases[row[1]]:
                yield (row[0], row[1], alias, row[3])
