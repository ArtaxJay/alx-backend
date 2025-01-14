#!/usr/bin/env python3
"""
Module for MRUCache
"""
from base_caching import BaseCaching
from collections import OrderedDict


class MRUCache(BaseCaching):
    """
    MRUCache is a caching system that follows the MRU
    (Most Recently Used) algorithm.
    """

    def __init__(self):
        """
        Initialize the cache.
        """
        super().__init__()
        # Use OrderedDict to maintain access order
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """
        Add an item to the cache.
        If the number of items exceeds MAX_ITEMS,
        discard the most recently used item (MRU).
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Remove the key to update its position in the access order
            self.cache_data.pop(key)

        self.cache_data[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Discard the most recently used item
            # (last item in OrderedDict)
            discarded_key, _ = self.cache_data.popitem(last=True)
            print(f"DISCARD: {discarded_key}")

    def get(self, key):
        """
        Retrieve an item by key from the cache.
        If key is None or the key doesn't exist, return None.
        """
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed key to the end to mark it as most recently used
        value = self.cache_data.pop(key)
        self.cache_data[key] = value
        return value
