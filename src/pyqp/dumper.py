#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain


class TableProvDumper(object):

    def __init__(self, version):
        self._version = version

    def __call__(self, table):
        print "\n".join(chain(self._draw_header(table), self._draw_rows(table)))

    def _draw_header(self, table):
        yield self._version
        yield ','.join([column.name for column in table.columns])
        yield ','.join([column.type_name for column in table.columns])
        yield ','.join(['"%s"' % column.desc for column in table.columns])

    def _draw_rows(self, table):
        for row in table:
            yield ','.join(map(str, row.values()))
