#!/usr/bin/env python
# -*- coding: utf-8 -*-
from operator import itemgetter
from collections import deque
from time import time


class Abstract(object):

    def append(self, value):
        pass

    def __iter__(self):
        raise NotImplementedError("Implement")

    def __call__(self):
        raise NotImplementedError("Implement")


class Accumulate(deque, Abstract):

    def __init__(self, size):
        deque.__init__(self, [], size)

    def __call__(self):
        return Accumulate(self.maxlen)


class TimeLimit(Abstract):

    def __init__(self, timeout):
        self._timeout = timeout
        self._getter = itemgetter(1)
        self._deque = deque([])

    def append(self, value):
        self._deque.append((time(), value))

    def __call__(self):
        return TimeLimit(self._timeout)

    def __iter__(self):
        treshold = time() - self._timeout
        while len(self._deque) > 0 and self._deque[0][0] < treshold:
            self._deque.popleft()
        return (self._getter(i) for i in self._deque)


class Resettable(Abstract):

    def __init__(self, check_func):
        self._should_be_reset = check_func
        self._list = []

    def __call__(self):
        return Resettable(self._shoudl_be_reset)

    def __iter__(self):
        if self._should_be_reset(self):
            self._list = []
        return iter(self._list)

    def append(self, value):
        self._list.append(value)
