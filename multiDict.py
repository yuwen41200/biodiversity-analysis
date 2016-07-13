#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class MultiDict(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super().__setitem__(key, [])
        self[key].append(value)
