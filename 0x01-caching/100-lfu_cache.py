#!/usr/bin/env python3
"""
Module for LFUCache
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache is a caching system that follows the LFU
    (Least Frequently Used) algorithm.
    If there are ties in frequency,
    it uses LRU to determine which item to discard.
    """

    def __init__(self):
        """
        Initialize the cache.
        """
        super().__init__()
        self.frequency = {}  # Track frequency of access for each key
        self.usage_order = []  # Track order of usage for LRU handling

    def put(self, key, item):
        """
        Add an item to the cache.
        If the number of items exceeds MAX_ITEMS,
        discard the least frequently used item (LFU).
        If there are ties in frequency,
        discard the least recently used item (LRU).
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update item and frequency
            self.cache_data[key] = item
            self.frequency[key] += 1
            # Move key to the end to mark it as recently used
            self.usage_order.remove(key)
            self.usage_order.append(key)
        else:
            # Add new item
            self.cache_data[key] = item
            self.frequency[key] = 1
            self.usage_order.append(key)

            # Check if we need to discard an item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # Find the least frequently used item(s)
                min_freq = min(self.frequency.values())
                least_frequent = [k for k, v in self.frequency.items()
                                  if v == min_freq]

                # If there's a tie, use LRU to decide which to discard
                if len(least_frequent) > 1:
                    for k in self.usage_order:
                        if k in least_frequent:
                            key_to_discard = k
                            break
                else:
                    key_to_discard = least_frequent[0]

                # Remove the chosen key
                del self.cache_data[key_to_discard]
                del self.frequency[key_to_discard]
                self.usage_order.remove(key_to_discard)
                print(f"DISCARD: {key_to_discard}")

    def get(self, key):
        """
        Retrieve an item by key from the cache.
        If key is None or the key doesn't exist, return None.
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and usage order
        self.frequency[key] += 1
        self.usage_order.remove(key)
        self.usage_order.append(key)

        return self.cache_data[key]
