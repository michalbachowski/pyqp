#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

# version is a human-readable version number.
__version__ = '0.1.0'
version = __version__

# version_info is a four-tuple for programmatic comparison. The first
# three numbers are the components of the version number.  The fourth
# is zero for an official release, positive for a development branch,
# or negative for a release candidate or beta (after the base version
# number has been incremented)
version_info = (0, 1, 0, -100)

from pyqp.column import Column
from pyqp.tables import Table
