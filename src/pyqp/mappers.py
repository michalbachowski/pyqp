#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DictRow(object):

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


def single_value(data):
    yield (data[0], frozenset(data[1]), data[2], data[3])


def values_list(data):
    for value in data:
        yield (value[0], frozenset(value[1]), value[2], value[3])


class DecoratorAbstract(object):

    def __init__(self, decorated):
        self._decorated = decorated

    def __call__(self, data):
        for row in self._decorated(data):
            for value in self._map(row):
                yield value

    def _map(self, value):
        raise NotImplementedError()


class Alias(DecoratorAbstract):

    def __init__(self, decorated, aliases):
        self._aliases = aliases
        DecoratorAbstract.__init__(self, decorated)

    def _map(self, row):
        yield row
        if row[2] not in self._aliases:
            return
        for alias in self._aliases[row[2]]:
            yield (row[0], row[1], alias, row[3])


class Select(DecoratorAbstract):

    def __init__(self, decorated, allowed):
        self._allowed = allowed
        DecoratorAbstract.__init__(self, decorated)

    def _map(self, row):
        if row[2] in self._allowed:
            yield row
        return


class Exclude(DecoratorAbstract):

    def __init__(self, decorated, excluded):
        self._excluded = excluded
        DecoratorAbstract.__init__(self, decorated)

    def _map(self, row):
        if row[2] in self._excluded:
            return
        yield row
