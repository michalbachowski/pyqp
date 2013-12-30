#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque


class Abstract(object):

    def append(self, value):
        pass

    def __call__(self):
        raise NotImplementedError("Implement")


class Accumulate(deque, Abstract):

    def __init__(self, size):
        deque.__init__(self, [], size)

    def __call__(self):
        return Accumulate(self.maxlen)
