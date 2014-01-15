#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from .columns import Column
from .configurators import simple_dict_factory, list_of_dicts_to_list_of_tuples,\
                    aggregate_filter, make_forwardable, set_default_dumper
from .tables import Table
from .mappers import dict_row, single_value, values_list, Keys
from .mappers.filters import alias, exclude
from .reducers import mean
from .aggregate import Accumulate
from .event_dispatcher import Dispatcher
from .dumpers import csv_dumper, decorated_dumper
from .dumpers.decorators import prepend, write_to_stdout

mappers = [\
    ('test', dict_row(('query_id',)), [\
        alias(success=['success_1h', 'success_1d']),\
        alias(Keys.TABLE_NAME, test=['query_quality']),\
        exclude('success'),\
        exclude('test', key=Keys.TABLE_NAME)]),
    ('pyqp_cell_value', single_value, []),\
    ('pyqp_cell_list', values_list, [])
]

tables = [
    {
        'aggregate_locally': True,
        'dumper': decorated_dumper(csv_dumper, \
                                            [prepend('1.23'), write_to_stdout]),
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

config_filters = aggregate_filter(simple_dict_factory, \
        make_forwardable(allow_forwarding, 'proxy_instance'), \
        set_default_dumper(decorated_dumper(csv_dumper, [write_to_stdout])))

d = Dispatcher()

for (table, drawer, config) in map(lambda x: config_filters(*x), \
                                    list_of_dicts_to_list_of_tuples(tables)):
    forwardable_tables[table.name] = not config.get('aggregate_locally', True)
    d.add_table(table, drawer)


for (event_name, mapper, filters) in mappers:
    d.add_mapper(event_name, mapper, filters)

######
# invoke test
######
d.dispatch('test', {'query_id': 1, 'last_succeded': 2, 'runtime': 3, 'success': 4})
d.dispatch('test', {'query_id': 1, 'last_succeded': 22, 'runtime': 9, 'success': 1})
d.dispatch('test', {'query_id': 2, 'last_succeded': 44, 'runtime': 9, 'success': 1})
d.dispatch('pyqp_cell_value', ('query_quality', 2, 'runtime', 1))
d.dispatch('pyqp_cell_list', [('query_quality', 1, 'runtime', 4)])
d.process()
