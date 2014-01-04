#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from functools import wraps
from itertools import chain


def csv_dumper(table):
    return "\n".join(chain([\
        ','.join([column.name for column in table.columns]),\
        ','.join([column.type_name for column in table.columns]),\
        ','.join(['"%s"' % column.desc for column in table.columns])],\
        [','.join(map(str, row.values())) for row in table]))


def prefix_dumper(base_dumper, prefix):
    p = str(prefix)
    @wraps(prefix_dumper)
    def _dumper(table):
        return p + "\n" + base_dumper(table)
    return _dumper


def file_dumper(base_dumper, file_name):
    @wraps(file_dumper)
    def _dumper(table):
        with open(file_name, 'w') as f:
            data = base_dumper(table)
            f.write(data)
        return data
    return _dumper


def stdout_dumper(base_dumper):
    @wraps(stdout_dumper)
    def _dumper(table):
        data = base_dumper(table)
        sys.stdout.write(data)
        return data
    return _dumper
