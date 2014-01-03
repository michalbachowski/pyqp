#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from itertools import chain


class CsvDumper(object):

    def __call__(self, table):
        return "\n".join(chain(self._draw_header(table), self._draw_rows(table)))

    def _draw_header(self, table):
        yield ','.join([column.name for column in table.columns])
        yield ','.join([column.type_name for column in table.columns])
        yield ','.join(['"%s"' % column.desc for column in table.columns])

    def _draw_rows(self, table):
        for row in table:
            yield ','.join(map(str, row.values()))


class TableProvDumper(CsvDumper):

    def __init__(self, version):
        self._version = version

    def __call__(self, table):
        return str(self._version) + "\n" + CsvDumper.__call__(self, table)


class FileDumper(object):

    def __init__(self, base_dumper, file_name):
        self._base_dumper = base_dumper
        self._file_name = file_name

    def __call__(self, table):
        with open(self._file_name, 'w') as f:
            return self._dump(f, table)

    def _dump(self, file_handler, table):
        data = self._base_dumper(table)
        file_handler.write(data)
        return data


class StdOutDumper(FileDumper):

    def __init__(self, base_dumper):
        FileDumper.__init__(self, base_dumper, None)

    def __call__(self, table):
        return self._dump(sys.stdout, table)
