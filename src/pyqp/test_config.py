#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .table import Table, TableForward
from .mappers import Alias, Direct
from .reducers import avg, last
from .aggregate import Accumulative
from .event_dispatcher import Dispatcher
from .drawer import TableDrawer
from functools import partial

mappers = [('test', Alias(Direct('query_quality', ('query_id',)), {'success': ['success_1h', 'success_1d']}))]

tables = {
    'query_quality': {
        'aggregate_on': 'machine',
        'version': '1.23',
        'columns': [
            'query_id', \
            ('last_succeded', last), \
            ('runtime', avg), \
            ('success_1h', sum), \
            ('success_1d', sum, Accumulative(1440))
        ]
    }
}


qq = Table('query_quality', [
    'query_id', \
    ('last_succeded', last), \
    ('runtime', avg), \
    ('success_1h', sum), \
    ('success_1d', sum, Accumulative(1440))
])

table_class = {'machine': Table, 'leader': partial(TableForward, 'some bus instance')}
d = Dispatcher()

for (table_name, conf) in tables.items():
    t = table_class[conf['aggregate_on']](table_name, conf['columns'])
    td = TableDrawer(conf['version'])
    d.add_table(t, td)

for (event_name, mapper) in mappers:
    d.add_mapper(event_name, mapper)

# test
d.dispatch('test', {'query_id': 1, 'last_succeded': 2, 'runtime': 3, 'success': 4})
d.dispatch('test', {'query_id': 1, 'last_succeded': 22, 'runtime': 9, 'success': 1})
d.dispatch('test', {'query_id': 2, 'last_succeded': 22, 'runtime': 9, 'success': 1})
d.process()
