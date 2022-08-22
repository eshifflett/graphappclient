from graphappclient.constants import (ACCESS_TOKEN, DEFAULT_SCOPE, ERROR, LOGIN_AUTH_URL)
import logging
from msal import ConfidentialClientApplication
import requests
from requests import Response

# Logger
logger = logging.getLogger(__name__)

class APIConnector:

    """
    This class is the main connection to the Graph API. It both makes all of the
    API calls and manages the access tokens with the crendentials provided from
    Microsoft.

    Attributes
        msal_app(ConfidentialClientApplication): The MSAL object that is used
            to get and manage auth tokens with the Graph API
    """

    def __init__(self, client_id: str, tenant_id: str, client_secret: str):
        """
        Initializes an APIConnector object. This class will handle managing
        auth tokens as well as making the HTTP requests to the Graph API

        Parameters
            client_id : str
                Client ID of application registered in Azure
            tenant_id : str
                Tenant ID of application registered in Azure
            client_secret : str
                Client secret value of application registered in Azure
        """

        # MSAL object for managing access tokens
        self.msal_app = ConfidentialClientApplication(
            client_id,
            authority=f'{LOGIN_AUTH_URL}{tenant_id}',
            client_credential=client_secret
        )

        self._access_token = None

    def authenticate(self) -> bool:
        """
        Authenticates the GraphAppClient with Microsoft in order to make calls
        to the Graph API

        Returns
            bool:
                Boolean indicating the success of the authentication operation
        """
        logger.info('Attempting to authenticate...')

        tok = None
        tok = self._get_token()
        self._access_token = tok
        return False if tok == None else True
    
    def _get_token(self) -> str:
        """
        Leverages MSAL to either fetch token from cache or get token from MS

        Returns
            str:
                string representation of auth token to use
        """
        # First checking cache
        res = self.msal_app.acquire_token_silent(DEFAULT_SCOPE, None)
        if res == None or ERROR in res or ACCESS_TOKEN not in res:
            logger.info('No token found in cache. Attempting to fetch from ' +
            'Microsoft API')
            if res and ERROR in res:
                logger.error(res[ERROR])
        else:
            self._access_token = res[ACCESS_TOKEN]
            return res[ACCESS_TOKEN]
        
        # Fetching auth token from Microsoft
        res = self.msal_app.acquire_token_for_client(
            scopes=DEFAULT_SCOPE
        )
        # Checking for success
        if res == None or ERROR in res or ACCESS_TOKEN not in res:
            logger.error('An error occurred when fetching the access token from'
            + ' Microsoft.')
            if res and ERROR in res:
                logger.error(res[ERROR])
        else:
            self._access_token = res[ACCESS_TOKEN]
            return res[ACCESS_TOKEN]
        
        return None # No token found
    
    def _get_headers(self) -> dict:
        """
        Creates and returns headers JSON object to be sent with HTTP requests
        for authentication with Microsoft.

        Returns
            dict:
                JSON representing auth bearer token header
        """
        # Get auth token for call
        token = self._get_token()
        headers = {'Authorization': 'Bearer ' + token}
        return headers
    
    def get(self, url: str) -> Response:
        """
        Used for making GET API calls to MS Graph

        Parameters
            url : str
                URL endpoint to GET from
        """
        # Get auth token for call
        headers = self._get_headers()

        return requests.get(url, headers=headers)
    
    def post(self, url: str, json: dict=None) -> Response:
        """
        Used for making POST API calls to MS Graph

        Parameters
            url : str
                URL endpoint to GET from
            data : Union[dict, None]
                JSON to be sent in POST
        """
        # Get auth token for call
        headers = self._get_headers()

        return requests.post(url, json=json, headers=headers)
    
    def delete(self, url: str, json: dict=None) -> Response:
        """
        Used for making delete API calls to MS Graph

        Parameters
            url : str
                URL endpoint to GET from
            data : Union[dict, None]
                JSON to be sent in call
        """
        # Get auth token for call
        headers = self._get_headers()

        return requests.delete(url, json=json, headers=headers)

    def patch(self, url: str, json: dict=None) -> Response:
        """
        Used for making PATCH API calls to MS Graph

        Parameters
            url : str
                URL endpoint to GET from
            data : Union[dict, None]
                JSON to be sent in call
        """
        # Get auth token for call
        headers = self._get_headers()

        return requests.patch(url, json=json, headers=headers)
