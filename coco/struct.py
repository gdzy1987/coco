#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import queue
import socket


class MultiQueueMixin:
    def mget(self, size=1, block=True, timeout=5):
        items = []
        for i in range(size):
            try:
                items.append(self.get(block=block, timeout=timeout))
            except queue.Empty:
                break
        return items

    def mput(self, data_set):
        for i in data_set:
            self.put(i)


class MemoryQueue(MultiQueueMixin, queue.Queue, object):
    pass


class SizedList(list):
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        self.size = 0
        self.end_with_ascii = False
        super(list, self).__init__()

    def is_full(self):
        if self.maxsize == 0:
            return False
        if not self.end_with_ascii:
            return False
        if self.size >= self.maxsize:
            return True
        else:
            return False

    def append(self, b):
        if not self.is_full():
            super(SizedList, self).append(b)
            self.size += len(b)
            self.end_with_ascii = b[-1] <= 126

    def clean(self):
        self.size = 0
        del self[:]


class SelectEvent:
    def __init__(self):
        self.p1, self.p2 = socket.socketpair()

    def set(self):
        self.p2.send(b'0')

    def fileno(self):
        return self.p1.fileno()

    def __getattr__(self, item):
        return getattr(self.p1, item)
