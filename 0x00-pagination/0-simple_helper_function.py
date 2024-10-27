#!/usr/bin/env python3
"""Helper function to practice backend pagination"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Takes 2 int args and rets a tuple of 2: (start & end)
    Args:
        page (int): pg num 2 ret (pgs are 1-indexed)
        page_size (int): num of entities returned per pg
    Return:
        tuple(index_start, index_end)
    """
    index_start, index_end = 0, 0
    for i in range(page):
        index_start = index_end
        index_end += page_size

    return (index_start, index_end)
