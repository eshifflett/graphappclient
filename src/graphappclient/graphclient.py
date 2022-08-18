from http import HTTPStatus
import logging
import api_connector
from typing import List, Optional, Union
from user import User
from utils import APIBase

# Logger
logger = logging.getLogger(__name__)

class GraphAppClient(APIBase):

    _endpoints = {
        'get_users' : '/users',
        'get_user' : '/users/{id}'
    }

    def __init__(self, client_id: str, tenant_id: str, client_secret: str):
        """
        Initializes a GraphAppClient with given credentials (does not
        authenticate with Microsoft at initialization)

        Parameters
        client_id : str
            Client ID of application registered in Azure
        tenant_id : str
            Tenant ID of application registered in Azure
        client_secret : str
            Client secret value of application registered in Azure
        """
        # Super class constructor
        super().__init__()

        # Creating new connector object with auth information
        self.graph_connector = api_connector.APIConnector(
            client_id,
            tenant_id,
            client_secret
        )
    
    def __repr__(self):
        return f'Graph Client with Client ID: {self.graph_connector.msal_app.client_id}'
    
    def authenticate(self) -> bool:
        """
        Authenticates the GraphAppClient with Microsoft in order to make calls
        to the Graph API

        Returns
        bool
            Boolean indicating the success of the authentication operation
        """
        logger.info('Attempting to authenticate...')

        return self.graph_connector.authenticate()
    
    def get_users(self) -> Union[List[User], None]:
        """
        Gets and returns a list of User objects in the Microsoft organization

        Returns
        Union[List[user.User], None]
            A list of User objects if found, otherwise None
        """
        # Get endpoint URL
        graph_api_url = self.build_url(self._endpoints['get_users'])

        # Make API call
        response = self.graph_connector.get(graph_api_url)

        if not response.status_code == HTTPStatus.OK: # Checking for 200
            logger.error('Error when getting users from Graph API')
            logger.error(response.reason)
            return None
        
        user_json_list = response.json()['value']
        user_object_list = []
        
        for user_json in user_json_list:
            # Creating new User object
            new_user = User(
                self.graph_connector,
                user_json['businessPhones'],
                user_json['displayName'],
                user_json['givenName'],
                user_json['jobTitle'],
                user_json['mail'],
                user_json['mobilePhone'],
                user_json['officeLocation'],
                user_json['preferredLanguage'],
                user_json['surname'],
                user_json['userPrincipalName'],
                user_json['id']
            )

            # Adding to User list to return
            user_object_list.append(new_user)
        
        return user_object_list
    
    def get_user(self, user_id: Optional[str] = None,
                    user_principal_name: Optional[str] = None) -> Union[User, None]:
        """
        Gets user either via user ID or principal name. It will prioritize
        fetching via ID if both are provided.

        Parameters
        user_id : Optional[str]
            User ID to fetch user from. If not provided, the principal name
            is used instead
        user_principal_name : Optional[str]
            e.g. login username, another way to fetch users. Will be used only
            if user_id is not provided
        
        Returns
        Union[User, None]
            A User object if the user is found, None otherwise.
        
        Raises
        ValueError
            Raises this error if neither argument is provided
        """

        if user_id:
            # Build endpoint and URL
            user_fetch_endpoint = self._endpoints['get_user'].format(id=user_id)
            graph_api_url = self.build_url(user_fetch_endpoint)
        elif user_principal_name:
            # Build endpoint and URL
            user_fetch_endpoint = self._endpoints['get_user'].format(id=user_principal_name)
            graph_api_url = self.build_url(user_fetch_endpoint)
        else:
            raise ValueError('Either a user_id or a user_principal_name must'
                                + ' be provided.')

        # Make API call
        response = self.graph_connector.get(graph_api_url)
        if not response.status_code == HTTPStatus.OK: # Checking for 200
            logger.error('Error when getting user from Graph API')
            logger.error(response.reason)
            return None
        
        user_json = response.json()
        new_user = User(
            self.graph_connector,
            user_json['businessPhones'],
            user_json['displayName'],
            user_json['givenName'],
            user_json['jobTitle'],
            user_json['mail'],
            user_json['mobilePhone'],
            user_json['officeLocation'],
            user_json['preferredLanguage'],
            user_json['surname'],
            user_json['userPrincipalName'],
            user_json['id']
        )
        
        return new_user