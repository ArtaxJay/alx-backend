#!/usr/bin/env python3
"""
Creates a Server class for paginating a DB (Popular_Baby_Names.csv)
"""
import csv
from typing import List, Tuple


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


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Takes 2 ints args & rets requested pg from d csv file
        Args:
            page (int): pg num, a +ve int
            page_size (int): num of records per pg, a +ve int
        Return:
            list of lists from csv file that contains req. data
        """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0

        csv_file_data = self.dataset()
        try:
            index = index_range(page, page_size)
            return csv_file_data[index[0]:index[1]]
        except IndexError:
            return []


    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Takes two args and rets the req data in dict(key-value, json) format
        Args:
            page (int): current pg numb
            page_size (int): whole pg size
        Returns:
            List[List]: key-value pair dict of data
        """
        total_pages = len(self.dataset()) // page_size + 1
        data = self.get_page(page, page_size)
        popular_baby_names = {
            "page": page,
            "page_size": page_size if page_size <= len(data) else len(data),
            "total_pages": total_pages,
            "data": data,
            "prev_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if page + 1 <= total_pages else None
        }
        return popular_baby_names
