from graphappclient.api_connector import APIConnector
from graphappclient.constants import (API_VERSION, GRAPH_BASE_URL, NEXT_ODATA,
                                    VALUE)
from http import HTTPStatus
import logging
from typing import Any, List

# Logger
logger = logging.getLogger(__name__)

class APIBase:
    """
    Base class for all classes that have API calls, will include functions that
    are useful to all such classes, such as building a URL for API calls

    Attributes
        base_url(str): Base URL for Graph API calls
    """

    def __init__(self):
        """
        Initializes APIBase object. This will be inherited by any class that
        makes Graph API calls, and holds some utilities that all of them will
        need.
        """

        self.base_url = self._build_base_url(
            GRAPH_BASE_URL,
            API_VERSION
        )
    
    def _build_base_url(self, url: str, ver: str) -> str:
        """
        Builds the base URL for calls to the Graph API

        Parameters
            url : str
                Base url for Graph API
            ver : str
                Version of Graph API to be used

        Returns
            str:
                String representation of base URL for Graph API calls
        """
        return f'{url}{ver}'
    
    def build_url(self, endpoint: str) -> str:
        """
        Builds URL for Graph API call

        Parameters
            endpoint : str
                Endpoint being called

        Returns
            str:
                String representation of the url for API call
        """
        return f'{self.base_url}{endpoint}'


class Paginator(APIBase):
    """
    Custom data structure used to support pagination of data from Graph API
    request responses. It's iterable, so you can iterate over the whole
    collection of returned data Pythonically and it will request more data
    as the current page runs out. You can also access pages individually and
    call get_next_page() to manually manage pages.

    Attributes
        graph_connector(APIConnector): Manages access tokens and makes API calls
        page(List): Current page of data returned
        next_page_url(str): URL to GET for next page of data
        constructor(Any): Constructor to create objects from MS data
        limit(int): Max total data entries to be returned
    """
    def __init__(
        self,
        api_connector: APIConnector,
        data: List,
        next_page_url: str,
        constructor: Any,
        limit: int = None
    ):
        """
        Initializes Paginator object. This is a data structure that supports
        iteration, and will automatically fetch each page if iterated over like
        a list

        Parameters
            api_connector : APIConnector
                Manages access tokens and makes API calls
            data : List
                First page of data
            next_page_url : str
                URL to GET for next page of data
            constructor : Any
                Constructor to create objects from MS data
            limit : int
                Max total data entries to be returned
        """

        # Super class constructor
        super().__init__()
        
        self.graph_connector = api_connector
        self.page = data
        self._idx = 0
        self.next_page_url = next_page_url
        self.constructor = constructor
        self.limit = limit

        if limit and limit < len(data): # received more than limit
            self.curr_data_count = self.total_data_count = limit
        else:
            self.curr_data_count = self.total_data_count = len(data)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        # Checking if we can just index data
        if self._idx < self.curr_data_count:
            val = self.page[self._idx]
            self._idx += 1
            return val
        elif self.limit and self.limit <= self.total_data_count:
            raise StopIteration()
        
        # Checking if there's more data to fetch
        if self.next_page_url == None:
            raise StopIteration()
        
        # Fetching next page
        response = self.graph_connector.get(self.next_page_url)
        if not response.status_code == HTTPStatus.OK: # Checking for 200
            logger.error('Error when getting next page from Graph API')
            logger.error(response.content)
            raise StopIteration()
        
        # Get JSON
        response_data = response.json()

        # Check for next page URL
        self.next_page_url = response_data.get(NEXT_ODATA, None)

        # Get list of JSON's to be deserialized
        returned_list = response_data.get(VALUE, [])

        # Check for callable constructor
        if callable(self.constructor):
            self.page = []
            for item in returned_list:
                self.page.append(self.constructor(self.graph_connector, item))
        else:
            raise StopIteration()
        
        returned_list_count = len(self.page)
        if self.limit and self.limit < len(self.page) + self.total_data_count: # received more than limit 
            self.next_page_url = None
            self.curr_data_count = len(self.page) + self.total_data_count - self.limit
            self.total_data_count += self.curr_data_count
            returned_list_count = self.curr_data_count
        
        if returned_list_count > 0: # cleanup and returning value
            self.curr_data_count = returned_list_count
            self.total_data_count += returned_list_count
            self._idx = 0
            val = self.page[self._idx]
            self._idx += 1
            return val
        else:
            raise StopIteration()
    
    def next_page(self) -> bool:
        """
        Gets the next page of data requested from Microsoft. This will set the
        page attribute to the next list of data

        Returns:
            bool:
                Indicates the success of the operation
        """
        if self.next_page_url == None: # No more pages to get
            return False
        
        # Fetching next page
        response = self.graph_connector.get(self.next_page_url)
        if not response.status_code == HTTPStatus.OK: # Checking for 200
            logger.error('Error when getting next page from Graph API')
            logger.error(response.content)
            return False
        
        # Get JSON
        response_data = response.json()

        # Check for next page URL
        self.next_page_url = response_data.get(NEXT_ODATA, None)

        # Get list of JSON's to be deserialized
        returned_list = response_data.get(VALUE, [])

        # Check for callable constructor
        if callable(self.constructor):
            self.page = []
            for item in returned_list:
                self.page.append(self.constructor(self.graph_connector, item))
        else:
            return False
        
        returned_list_count = len(self.page)
        if self.limit and self.limit < len(self.page) + self.total_data_count: # received more than limit 
            self.next_page_url = None
            self.curr_data_count = len(self.page) + self.total_data_count - self.limit
            self.total_data_count += self.curr_data_count
            returned_list_count = self.curr_data_count
        
        if returned_list_count > 0: # cleanup and returning value
            self.curr_data_count = returned_list_count
            self.total_data_count += returned_list_count
            self._idx = 0
            return True
        else:
            return False