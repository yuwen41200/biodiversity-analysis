#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urlencode
from urllib import request
import threading, json

class speciesQuery:

    API_GBIF = "http://api.gbif.org/v1/species"

    def __init__(self, species, callback, callbackArgs):
        """
        Query from GBIF detailed info of a given species, asynchronously

        :param species: name of species to be looked up
        :param callback: Callback function when lookup returns
        :param callbackArgs: arguments for callback function
        """

        thread = threading.Thread(target=self.lookUp, args=(species, callback, callbackArgs), daemon=True)
        thread.start()

    def lookUp(self, species, callback, callbackArgs):
        """
        Evoke GBIF API to look up for a species

        :param species: name of species to be looked up
        :param callback: Callback function when lookup returns
        :param callbackArgs: arguments for callback function
        :return: None.
        """

        url = self.API_GBIF + "?" + urlencode({"name": species})

        try:
            conn = request.urlopen(url)
            if not conn.getcode() is 200:
                return
        except:
            return

        try:
            results = json.loads(conn.read().decode("utf-8"))["results"]
            if not results:
                return
        except:
            return

        callback(results[0], *callbackArgs)
