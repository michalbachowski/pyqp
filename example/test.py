#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyqp.columns import Column
from pyqp.configurators import simple_dict_config, list_of_configs, filtered_configurator
from pyqp.configurators.columns import default_column_factory
from pyqp.configurators.filters import aggregate_filter, make_forwardable, \
                                                            set_default_dumper
from pyqp.tables import Table
from pyqp.mappers import dict_row, single_value, values_list, filtered_mapper, Keys
from pyqp.mappers.filters import aggregate_filter as af2, alias, exclude
from pyqp.reducers import mean
from pyqp.aggregate import Accumulate
from pyqp.event_dispatcher import Dispatcher
from pyqp.dumpers import csv_dumper, filtered_dumper
from pyqp.dumpers.filters import aggregate_filter as af, prepend, write_to_stdout

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

d = Dispatcher()

for (table, drawer, config) in configurator(tables):
    forwardable_tables[table.name] = not config.get('aggregate_locally', True)
    d.add_table(table, drawer)


for (event_name, mapper) in mappers.items():
    d.add_mapper(event_name, mapper)

######
# invoke test
######
d.dispatch('test', {'query_id': 1, 'last_succeded': 2, 'runtime': 3, 'success': 4})
d.dispatch('test', {'query_id': 1, 'last_succeded': 22, 'runtime': 9, 'success': 1})
d.dispatch('test', {'query_id': 2, 'last_succeded': 44, 'runtime': 9, 'success': 1})
d.dispatch('pyqp_cell_value', ('query_quality', 2, 'runtime', 1))
d.dispatch('pyqp_cell_list', [('query_quality', 1, 'runtime', 4)])
d.process()
