#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from .column import Column
from .configurators import simple_dict_factory, list_of_dicts_to_list_of_tuples,\
                    aggregate_filter, dbus_forwardable, set_default_drawer
from .table import Table
from .mappers import dict_row, single_value, values_list, Keys
from .filters import alias, exclude
from .reducers import mean
from .aggregate import Accumulate
from .event_dispatcher import Dispatcher
from .dumper import prefix_dumper, csv_dumper, stdout_dumper

mappers = [\
    ('test',
        exclude(
            exclude(
                alias(
                    alias(
                        dict_row(('query_id',)),
                        {'success': ['success_1h', 'success_1d']}
                    ),
                    {'test': ['query_quality']},
                    Keys.TABLE_NAME
                ),
                ['success']
            ),
            ['test'],
            Keys.TABLE_NAME
        )
    ),
    ('pyqp_cell_value', single_value),\
    ('pyqp_cell_list', values_list)
]

tables = [
    {
        'aggregate_locally': True,
        'drawer': stdout_dumper(prefix_dumper(csv_dumper, '1.23')),
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

config_filters = aggregate_filter(simple_dict_factory, \
        dbus_forwardable(is_leader, 'proxy_instance'), \
        set_default_drawer(stdout_dumper(csv_dumper)))

d = Dispatcher()

for (table, drawer, config) in map(lambda x: config_filters(*x), \
                                    list_of_dicts_to_list_of_tuples(tables)):
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
