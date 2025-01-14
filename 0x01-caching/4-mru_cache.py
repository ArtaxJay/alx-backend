#!/usr/bin/env python3
"""
Module for MRUCache
"""
from base_caching import BaseCaching


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
        self.usage_order = []  # Keep track of the usage order

    def put(self, key, item):
        """
        Add an item to the cache.
        If the number of items exceeds MAX_ITEMS,
        discard the most recently used item (MRU).
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Remove key from usage_order as it will be re-added
            self.usage_order.remove(key)

        self.cache_data[key] = item
        self.usage_order.append(key)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            # Discard the most recently used item (last in usage_order)
            most_recent_key = self.usage_order.pop(-2)
            del self.cache_data[most_recent_key]
            print(f"DISCARD: {most_recent_key}")

    def get(self, key):
        """
        Retrieve an item by key from the cache.
        If key is None or the key doesn't exist, return None.
        """
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed key to the end to mark it as most recently used
        self.usage_order.remove(key)
        self.usage_order.append(key)
        return self.cache_data[key]
