#!/usr/bin/env python3
"""
Module for FIFOCache
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache is a caching system that follows the FIFO algorithm.
    """

    def __init__(self):
        """
        Initialize the cache.
        """
        super().__init__()
        self.keys = []  # List to maintain the order of insertion

    def put(self, key, item):
        """
        Add an item to the cache.
        If the number of items exceeds MAX_ITEMS, --
        --remove the first item added (FIFO).
        """
        if key is not None and item is not None:
            if key in self.cache_data:
                self.keys.remove(key)  # Remove the key if it already exists

            self.cache_data[key] = item
            self.keys.append(key)

            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                oldest_key = self.keys.pop(0)  # Remove the first key added
                del self.cache_data[oldest_key]
                print(f"DISCARD: {oldest_key}")

    def get(self, key):
        """
        Retrieve an item by key from the cache.
        If key is None or the key doesn't exist, return None.
        """
        return self.cache_data.get(key, None)
