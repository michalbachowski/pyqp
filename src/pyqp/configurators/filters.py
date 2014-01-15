#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial, wraps
from itertools import chain
from pyqp.tables.decorators import TableForwarder

def aggregate_filter(*filters):

    def _apply_filters(output, filter_func):
        return chain.from_iterable(map(lambda item: filter_func(*item), output))

    @wraps(aggregate_filter)
    def _filter(table, dumper, config):
        return reduce(_apply_filters, filters, [(table, dumper, config)])
    return _filter


def decorate_table(allow_decorating, decorator):
    @wraps(decorate_table)
    def _filter(table, dumper, config):
        if allow_decorating(config):
            table = decorator(table)
        yield (table, dumper, config)
    return _filter


def make_forwardable(allow_forwarding, proxy):
    return decorate_table(lambda c: True, partial(TableForwarder, proxy=proxy, \
                                            allow_forwarding=allow_forwarding))


def set_default_dumper(default_dumper):
    @wraps(set_default_dumper)
    def _filter(table, dumper, config):
        if dumper is None:
            dumper = default_dumper
        yield (table, dumper, config)
    return _filter
