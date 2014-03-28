#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyqp import Column, Table
from pyqp.reducers import mean
from pyqp.aggregate import Accumulate

# create table instance
table = Table('query_quality', [
    Column('query_id'),
    Column('foo'),
    Column(name='last_succeded'),
    Column('runtime', mean, Accumulate(60)),
    Column('success_1h', sum, Accumulate(60)),
    Column('success_1d', sum, Accumulate(1440))])

# add values
table.add_value(1, 'query_id', 1)\
    .add_value(1, 'last_succeded', 2)\
    .add_value(1, 'runtime', 3)\
    .add_value(1, 'success_1h', 4)\
    .add_value(1, 'success_1d', 4)

table.add_value(1, 'query_id', 1)\
    .add_value(1, 'last_succeded', 22)\
    .add_value(1, 'runtime', 9)\
    .add_value(1, 'success_1h', 1)\
    .add_value(1, 'success_1d', 1)

table.add_value(2, 'query_id', 2)\
    .add_value(2, 'last_succeded', 44)\
    .add_value(2, 'runtime', 9)\
    .add_value(2, 'success_1h', 1)\
    .add_value(2, 'success_1d', 1)

table.add_value(1, 'runtime', 4)\
    .add_value(2, 'runtime', 1)

# dump
print [[col.reduce() for col in row] for row in table]
