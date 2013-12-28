#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .table import Table
from .mappers import Direct
from .reducers import avg, last
from .aggregate import Accumulative
from .event_handler import Mapper
from .reactors import Local


qq = Table('query_quality', [
    'query_id', \
    ('last_succeded', last), \
    ('runtime', avg), \
    ('success_1h', sum), \
    ('success_1d', sum, Accumulative(1440))
])

m = Mapper()
m.add_table(qq).add_mapper('test', Direct('query_quality'))

r = Local().append(m)
