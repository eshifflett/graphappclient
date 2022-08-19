from graphappclient.constants import (API_VERSION, GRAPH_BASE_URL)

class APIBase:
    """
    Base class for all classes that have API calls, will include functions that
    are useful to all such classes, such as building a URL for API calls
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
        str
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
        str
            String representation of the url for API call
        """
        return f'{self.base_url}{endpoint}'