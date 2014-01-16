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


class Accumulate(deque):
    """Aggregator that accumulates values up to given size.
    When size is reached and new item is added - oldest value is deleted.
    This is just wrapper around collections.deque

    >>> a = Accumulate(2)
    >>> a.append(1)
    >>> a.append(2)
    >>> [i for i in a]
    [1, 2]
    >>> a.append(3)
    >>> [i for i in a]
    [2, 3]
    """

    def __init__(self, size):
        deque.__init__(self, [], size)


class TimeLimit(Abstract):
    """Aggregator that accumulates values for given amount of seconds.
    Outdated records are removed from list.

    >>> from time import sleep
    >>> t = TimeLimit(1)
    >>> t.append(1)
    >>> t.append(2)
    >>> [i for i in t]
    [1, 2]
    >>> t.append(3)
    >>> [i for i in t]
    [1, 2, 3]
    >>> sleep(2)
    >>> [i for i in t]
    []
    """

    def __init__(self, timeout):
        self._timeout = timeout
        self._getter = itemgetter(1)
        self._deque = deque([])

    def append(self, value):
        self._deque.append((time(), value))

    def __iter__(self):
        self._prune_old_rows()
        return (self._getter(i) for i in self._deque)

    def _prune_old_rows(self):
        treshold = time() - self._timeout
        while len(self._deque) > 0 and self._deque[0][0] < treshold:
            self._deque.popleft()


class Resettable(Abstract):
    """Aggregator that accumulates values until explicity resetted.
    Reset function is given internal list of values.
    Reset function is checked when Resettable.__iter__ is executed.

    >>> reset = lambda values: len(values) > 2
    >>> r = Resettable(reset)
    >>> r.append(1)
    >>> r.append(2)
    >>> [i for i in r]
    [1, 2]
    >>> r.append(3)
    >>> [i for i in r]
    []
    """

    def __init__(self, check_func):
        self._should_be_reset = check_func
        self._list = []

    def append(self, value):
        self._list.append(value)

    def __iter__(self):
        if self._should_be_reset(self._list):
            self._list = []
        return iter(self._list)
