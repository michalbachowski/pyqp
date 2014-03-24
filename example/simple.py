#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyqp import Column, Table
from pyqp.reducers import mean
from pyqp.aggregate import Accumulate

from pyqp.event_dispatcher import Dispatcher
from pyqp.mappers import dict_row, single_value, values_list, filtered_mapper, Keys
from pyqp.mappers.filters import aggregate_filter as af2, alias, exclude
from pyqp.dumpers import csv_dumper, filtered_dumper
from pyqp.dumpers.filters import aggregate_filter as af, prepend, write_to_stdout

def prepare():
    table = Table('query_quality', [
        Column('query_id'),
        Column('foo'),
        Column(name='last_succeded'),
        Column('runtime', mean, Accumulate(60)),
        Column('success_1h', sum, Accumulate(60)),
        Column('success_1d', sum, Accumulate(1440))])

    dumper = filtered_dumper(csv_dumper, af(prepend('1.23'), write_to_stdout))
    mapper = filtered_mapper(
            dict_row('query_id'),
            af2(
                alias(success=['success_1h', 'success_1d']),
                alias(Keys.TABLE_NAME, test=['query_quality']),
                exclude('success'),
                exclude('test', key=Keys.TABLE_NAME)
            )
        )
    return (table, dumper, mapper)

def main(dispatcher):
    (table, dumper, mapper) = prepare()
    dispatcher\
        .add_table(table, dumper)\
        .add_mapper('pyqp_cell_value', single_value)\
        .add_mapper('pyqp_cell_list', values_list)\
        .add_mapper('test', mapper)

######
# invoke test
######
if '__main__' == __name__:
    d = Dispatcher()
    main(d)
    d.dispatch('test', {'query_id': 1, 'last_succeded': 2, 'runtime': 3, 'success': 4})
    d.dispatch('test', {'query_id': 1, 'last_succeded': 22, 'runtime': 9, 'success': 1})
    d.dispatch('test', {'query_id': 2, 'last_succeded': 44, 'runtime': 9, 'success': 1})
    d.dispatch('pyqp_cell_value', ('query_quality', 2, 'runtime', 1))
    d.dispatch('pyqp_cell_list', [('query_quality', 1, 'runtime', 4)])
    d.process()
