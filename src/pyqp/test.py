#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .table import Table
from .mappers import Alias, Direct
from .reducers import avg, last
from .aggregate import Accumulative
from .event_dispatcher import Dispatcher
from .drawer import TableDrawer

qq = Table('query_quality', [
    'query_id', \
    ('last_succeded', last), \
    ('runtime', avg), \
    ('success_1h', sum), \
    ('success_1d', sum, Accumulative(1440))
])

m = Alias(Direct('query_quality', ('query_id',)), {'success': ['success_1h', 'success_1d']})

d = Dispatcher()
d.add_table(qq, TableDrawer('1.23')).add_mapper('test', m)

# test
d.dispatch('test', {'query_id': 1, 'last_succeded': 2, 'runtime': 3, 'success': 4})
d.dispatch('test', {'query_id': 1, 'last_succeded': 22, 'runtime': 9, 'success': 1})
d.dispatch('test', {'query_id': 2, 'last_succeded': 22, 'runtime': 9, 'success': 1})
d.process()
