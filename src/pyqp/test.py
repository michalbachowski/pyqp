#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .table import Table, TableForwarder
from .mappers import Translate, DictRow, single_value
from .reducers import avg, last
from .aggregate import Accumulative
from .event_dispatcher import Dispatcher
from .drawer import TableDrawer
from functools import partial

mappers = [\
    ('test',
        Translate(
            DictRow('query_quality', ('query_id',)),
            {'success': ['success_1h', 'success_1d']}
        )
    ),
    ('pyqp_cell_value', single_value),\
]

tables = [
    {
        'aggregate_on': 'machine',
        'drawer': TableDrawer('1.23'),
        'table': Table('query_quality', [
            'query_id', \
            ('last_succeded', last), \
            ('runtime', avg), \
            ('success_1h', sum), \
            ('success_1d', sum, Accumulative(1440)),\
        ])
    }
]


forwarder_class = partial(TableForwarder, 'some bus instance')
d = Dispatcher()

for conf in tables:
    t = conf['table']
    if conf['aggregate_on'] != 'machine':
        t = forwarder_class(t.name, t.columns)
    d.add_table(t, conf['drawer'])

for (event_name, mapper) in mappers:
    d.add_mapper(event_name, mapper)

# test
d.dispatch('test', {'query_id': 1, 'last_succeded': 2, 'runtime': 3, 'success': 4})
d.dispatch('test', {'query_id': 1, 'last_succeded': 22, 'runtime': 9, 'success': 1})
d.dispatch('test', {'query_id': 2, 'last_succeded': 22, 'runtime': 9, 'success': 1})
d.process()
