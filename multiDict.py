#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class MultiDict(dict):

    def __setitem__(self, key, value):
        """
        Override default dictionary behavior so that it can support duplicate keys.
        e.g. Inserting {'k': 'v1', 'k': 'v2'} will produce {'k': ['v1', 'v2']}.

        :param key: Key of the key-value pair to be inserted.
        :param value: Value of the key-value pair to be inserted.
        :return: None.
        """

        try:
            self[key]
        except KeyError:
            super().__setitem__(key, [])
        self[key].append(value)
