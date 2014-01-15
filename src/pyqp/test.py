#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from .columns import Column
from .configurators import simple_dict_factory, filtered_configurator
from .configurators.filters import aggregate_filter, make_forwardable, \
                                                            set_default_dumper
from .tables import Table
from .mappers import dict_row, single_value, values_list, filtered_mapper, Keys
from .mappers.filters import aggregate_filter as af2, alias, exclude
from .reducers import mean
from .aggregate import Accumulate
from .event_dispatcher import Dispatcher
from .dumpers import csv_dumper, filtered_dumper
from .dumpers.filters import aggregate_filter as af, prepend, write_to_stdout

mappers = [\
    ('test', filtered_mapper(dict_row(('query_id',)), af2(
        alias(success=['success_1h', 'success_1d']),\
        alias(Keys.TABLE_NAME, test=['query_quality']),\
        exclude('success'),\
        exclude('test', key=Keys.TABLE_NAME)))),
    ('pyqp_cell_value', single_value),\
    ('pyqp_cell_list', values_list)
]

tables = [
    {
        'aggregate_locally': True,
        'dumper': filtered_dumper(csv_dumper, af(prepend('1.23'), write_to_stdout)),
        'table': Table('query_quality', [
            'query_id', \
            {'name': 'last_succeded'}, \
            ('runtime', mean), \
            Column('success_1h', sum), \
            ('success_1d', sum, partial(Accumulate, 1440)),\
        ])
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

configurator = filtered_configurator(simple_dict_factory, aggregate_filter(\
        make_forwardable(allow_forwarding, 'proxy_instance'), \
        set_default_dumper(filtered_dumper(csv_dumper, af(write_to_stdout)))))

d = Dispatcher()

for (table, drawer, config) in configurator(tables):
    forwardable_tables[table.name] = not config.get('aggregate_locally', True)
    d.add_table(table, drawer)


for (event_name, mapper) in mappers:
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
