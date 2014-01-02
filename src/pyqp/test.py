#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .column import Column
from .configurators import dict_config_factory, list_config_reader, \
                    AggregateFilter, DbusForwardable, SetDefaultDrawer
from .table import Table
from .mappers import Translate, DictRow, single_value, values_list
from .reducers import avg
from .aggregate import Accumulate
from .event_dispatcher import Dispatcher
from .dumper import TableProvDumper

mappers = [\
    ('test',
        Translate(
            DictRow('query_quality', ('query_id',)),
            {'success': ['success_1h', 'success_1d']}
        )
    ),
    ('pyqp_cell_value', single_value),\
    ('pyqp_cell_list', values_list)
]

tables = [
    {
        'aggregate_locally': True,
        'drawer': TableProvDumper('1.23'),
        'table': Table('query_quality', [
            'query_id', \
            {'name': 'last_succeded'}, \
            ('runtime', avg), \
            Column('success_1h', sum), \
            ('success_1d', sum, Accumulate(1440)),\
        ])
    }
]

#######
# Configure instances
#
# DO NOT EDIT BELOW
#######

is_leader = True

config_filters = AggregateFilter() \
    .append(DbusForwardable(is_leader, 'dbus instance')) \
    .append(SetDefaultDrawer(TableProvDumper(1)))

d = Dispatcher()

for (table, drawer, config) in config_filters(dict_config_factory(\
                                                list_config_reader(tables))):
    d.add_table(table, drawer)


for (event_name, mapper) in mappers:
    d.add_mapper(event_name, mapper)

######
# invoke test
######
d.dispatch('test', {'query_id': 1, 'last_succeded': 2, 'runtime': 3, 'success': 4})
d.dispatch('test', {'query_id': 1, 'last_succeded': 22, 'runtime': 9, 'success': 1})
d.dispatch('test', {'query_id': 2, 'last_succeded': 44, 'runtime': 9, 'success': 1})
d.dispatch('pyqp_cell_value', ('query_quality', [2], 'runtime', 1))
d.dispatch('pyqp_cell_list', [('query_quality', [1], 'runtime', 4)])
d.process()
