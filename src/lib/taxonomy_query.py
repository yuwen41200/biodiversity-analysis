#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urlencode
from urllib.request import urlopen
from threading import Thread
from json import loads


# noinspection PyPep8Naming
class TaxonomyQuery:

    API_GBIF = "http://api.gbif.org/v1/species"

    def __init__(self, species, callback, callbackArgs):
        """
        Query detailed information of a given species from GBIF, asynchronously.

        :param species: Name of the species to be looked up.
        :param callback: Callback function when lookup returns.
        :param callbackArgs: Arguments for the callback function.
        """

        thread = Thread(target=self.lookUp, args=(species, callback, callbackArgs), daemon=True)
        thread.start()

    # noinspection PyBroadException
    def lookUp(self, species, callback, callbackArgs):
        """
        Evoke GBIF API to look up a species.

        :param species: Name of the species to be looked up.
        :param callback: Callback function when lookup returns.
        :param callbackArgs: Arguments for the callback function.
        :return: None.
        """

        url = self.API_GBIF + "?" + urlencode({"name": species})

        try:
            conn = urlopen(url)
            if not conn.getcode() is 200:
                return
        except:
            return

        try:
            results = loads(conn.read().decode("utf-8"))["results"]
            if not results:
                return
        except:
            return

        callback(species, results[0], *callbackArgs)
