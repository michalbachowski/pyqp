#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque


class Abstract(object):

    def append(self, value):
        pass

    def __call__(self):
        raise NotImplementedError("Implement")


class Accumulative(Abstract, deque):

    def __init__(self, size):
        self._size = size
        deque.__init__(self, list(), size)

    def __call__(self):
        return Accumulative(self._size)
