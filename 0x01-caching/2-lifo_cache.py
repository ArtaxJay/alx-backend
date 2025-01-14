#!/usr/bin/env python3
"""
Module for LIFOCache
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache is a caching system that follows the LIFO algorithm.
    """

    def __init__(self):
        """
        Initialize the cache.
        """
        super().__init__()
        self.last_key = None  # Keeps track of the last inserted key

    def put(self, key, item):
        """
        Add an item to the cache.
        If the number of items exceeds MAX_ITEMS, --
        --remove the last added item (LIFO).
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

            # Keep track of the last inserted key
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                if self.last_key:
                    del self.cache_data[self.last_key]
                    print(f"DISCARD: {self.last_key}")

            self.last_key = key  # Update the last inserted key

    def get(self, key):
        """
        Retrieve an item by key from the cache.
        If key is None or the key doesn't exist, return None.
        """
        return self.cache_data.get(key, None)
