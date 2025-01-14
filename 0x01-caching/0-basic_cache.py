#!/usr/bin/env python3
"""
Module for BasicCache
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache is a caching system with no limit.
    """

    def put(self, key, item):
        """
        Add an item to the cache.
        If key or item is None, do nothing.
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """
        Retrieve an item by key from the cache.
        If key is None or the key doesn't exist, return None.
        """
        return self.cache_data.get(key, None)
