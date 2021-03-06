#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyqp import Column, Table
from pyqp.reducers import mean
from pyqp.aggregate import Accumulate

from pyqp.manager import Manager
from pyqp.mappers import dict_row, single_value, values_list, filtered_mapper, Keys
from pyqp.mappers.filters import aggregate_filter as af2, alias, exclude
from pyqp.dumpers import csv_dumper, filtered_dumper
from pyqp.dumpers.filters import aggregate_filter as af, prepend, write_to_stdout

from pyqp.configurators import simple_dict_config, list_of_configs, filtered_configurator
from pyqp.configurators.columns import default_column_factory
from pyqp.configurators.filters import aggregate_filter, make_forwardable, \
                                                            set_default_dumper

mappers = {
    'test': filtered_mapper(
        dict_row('query_id'),
        af2(
            alias(success=['success_1h', 'success_1d']),
            alias(Keys.TABLE_NAME, test=['query_quality']),
            exclude('success'),
            exclude('test', key=Keys.TABLE_NAME)
        )
    ),
    'pyqp_cell_value': single_value,
    'pyqp_cell_list': values_list
}



tables = [
    {
        'aggregate_locally': True,
        'dumper': filtered_dumper(csv_dumper, af(prepend('1.23'), write_to_stdout)),
        'table': Table('query_quality', default_column_factory(
            'query_id', \
            'foo', \
            {'name': 'last_succeded'}, \
            ('runtime', mean, Accumulate(60)), \
            Column('success_1h', sum, Accumulate(60)), \
            ('success_1d', sum, Accumulate(1440)), \
        ))
    }
]

#######
# Configure instances
#
# DO NOT EDIT BELOW
#######

is_leader = True
forwardable_tables = {}
allow_forwarding = lambda table_name: forwardable_tables.get(table_name, False)

configurator = filtered_configurator(list_of_configs(simple_dict_config), \
    aggregate_filter(\
        make_forwardable(allow_forwarding, 'proxy_instance'), \
        set_default_dumper(filtered_dumper(csv_dumper, af(write_to_stdout)))\
    )\
)

m = Manager()

for (table, dumper, config) in configurator(tables):
    forwardable_tables[table.name] = not config.get('aggregate_locally', True)
    m.add_table(table, dumper)


for (event_name, mapper) in mappers.items():
    m.add_mapper(event_name, mapper)

######
# invoke test
######
m.dispatch('test', {'query_id': 1, 'last_succeded': 2, 'runtime': 3, 'success': 4})
m.dispatch('test', {'query_id': 1, 'last_succeded': 22, 'runtime': 9, 'success': 1})
m.dispatch('test', {'query_id': 2, 'last_succeded': 44, 'runtime': 9, 'success': 1})
m.dispatch('pyqp_cell_value', ('query_quality', 2, 'runtime', 1))
m.dispatch('pyqp_cell_list', [('query_quality', 1, 'runtime', 4)])
m.dump()
