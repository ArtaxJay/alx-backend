#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Accepts two int args and rets a dict
        Args:
            index(int): first required index
            page_size(int): required number of records per page
        Return:
            dict (key-value):
            index, next_index, page_size, & response data
        """
        csv_data = self.indexed_dataset()
        csv_data_length = len(csv_data)
        assert 0 <= index < csv_data_length
        user_query_response = {}
        data = []
        user_query_response['index'] = index
        for i in range(page_size):
            while True:
                current_page = csv_data.get(index)
                index += 1
                if current_page is not None:
                    break
            data.append(current_page)

        user_query_response['data'] = data
        user_query_response['page_size'] = len(data)
        if csv_data.get(index):
            user_query_response['next_index'] = index
        else:
            user_query_response['next_index'] = None
        return user_query_response
