#!/usr/bin/env python3
"""
Module for LFUCache
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache defines a caching system with LFU eviction algorithm.
    If multiple items have the same frequency,
    LRU is used to decide which one to discard.
    """

    def __init__(self):
        """
        Initialize the class with the parent's init method.
        """
        super().__init__()
        # List to track usage order for LRU when frequencies are tied
        self.usage = []
        self.frequency = {}  # Dictionary to track frequency of each cache key

    def put(self, key, item):
        """
        Cache a key-value pair, applying the LFU eviction algorithm.
        """
        if key is None or item is None:
            return  # Don't do anything if key or item is None

        # If the cache is full and the key is not already in cache
        if (len(self.cache_data) >= BaseCaching.MAX_ITEMS and
                key not in self.cache_data):

            # Find the least frequently used items
            lfu = min(self.frequency.values())
            lfu_keys = [k for k, v in self.frequency.items() if v == lfu]

            # If there are ties, use LRU to determine which item to discard
            if len(lfu_keys) > 1:
                lru_lfu = {k: self.usage.index(k) for k in lfu_keys}
                discard = min(lru_lfu, key=lru_lfu.get)
            else:
                discard = lfu_keys[0]

            # Print and discard the least used item
            print(f"DISCARD: {discard}")
            del self.cache_data[discard]
            del self.frequency[discard]
            del self.usage[self.usage.index(discard)]

        # Update frequency and usage for the current key
        if key in self.cache_data:
            # Update item and frequency
            self.cache_data[key] = item
            self.frequency[key] += 1
        else:
            # Add new item
            self.cache_data[key] = item
            self.frequency[key] = 1

        # Update the usage order to mark this key as recently used
        if key in self.usage:
            self.usage.remove(key)  # Remove the key to reinsert it at the end
        self.usage.append(key)

    def get(self, key):
        """
        Return the value linked to a given key, or None if not found.
        """
        if key is None or key not in self.cache_data:
            return None  # If key is not found, return None

        # Update the frequency and usage order
        self.frequency[key] += 1
        self.usage.remove(key)
        self.usage.append(key)

        return self.cache_data[key]
