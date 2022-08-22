from graphappclient.api_connector import APIConnector
from graphappclient.constants import (BUSINESS_PHONES, DISPLAY_NAME, GIVEN_NAME, ID,
                                    JOB_TITLE, MAIL, MOBILE_PHONE, OFFICE_LOCATION,
                                    PREFERRED_LANGUAGE, SURNAME, USER_PRINCIPAL_NAME,
                                    VALUE, NEXT_ODATA)
from graphappclient.user import User
from graphappclient.utils import APIBase, Paginator
from http import HTTPStatus
import logging
from typing import List, Optional, Union

# Logger
logger = logging.getLogger(__name__)

class GraphAppClient(APIBase):

    """
    This class will be the starting point for all interaction with the Graph
    API.

    Attributes
        graph_connector(APIConnector): Manages access tokens and
            makes API calls
    """

    GET_USERS = 'get_users'
    GET_USER = 'get_user'
    CREATE_USER = 'create_user'

    _endpoints = {
        GET_USERS : '/users',
        GET_USER : '/users/{id}',
        CREATE_USER : '/users'
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
        self.graph_connector = APIConnector(
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
            bool:
                Boolean indicating the success of the authentication operation
        """
        logger.info('Attempting to authenticate...')

        return self.graph_connector.authenticate()
    
    def get_users(
        self,
        page_size: Optional[int] = None,
        limit: Optional[int] = None
    ) -> Union[List[User], Paginator, None]:
        """
        Gets and returns a list of User objects in the Microsoft organization

        Parameters
            page_size : Optional[int]
                Size of each page of data to be returned from Microsoft API calls
            limit : Optional[int]
                Limit on how much data is returned from Microsoft

        Returns
            Union[List[User], Paginator, None]:
                A list or Pagination of User objects if found, otherwise None
        """
        # Get endpoint URL
        graph_api_url = self.build_url(self._endpoints[self.GET_USERS])

        # Checking for page size request
        if page_size != None:
            graph_api_url = f'{graph_api_url}?$top={page_size.__str__()}'

        # Make API call
        response = self.graph_connector.get(graph_api_url)

        if not response.status_code == HTTPStatus.OK: # Checking for 200
            logger.error('Error when getting users from Graph API')
            logger.error(response.content)
            return None
        
        response_data = response.json()

        # Gets list of User JSON's
        user_json_list = response_data.get(VALUE)

        # Checking limit
        limit_reached = False
        if len(user_json_list) > limit:
            user_json_list = user_json_list[:limit]
            limit_reached = True

        user_object_list = []
        for user_json in user_json_list:
            # Creating new User object
            new_user = User(self.graph_connector, user_json)

            # Adding to User list to return
            user_object_list.append(new_user)
        
        if NEXT_ODATA not in response_data or limit_reached:
            return user_object_list
        else: # time for pagination
            user_paginator = Paginator(
                self.graph_connector,
                user_object_list,
                response_data.get(NEXT_ODATA),
                User,
                limit=limit
            )
            return user_paginator
    
    def get_user(
        self,
        user_id: Optional[str] = None,
        user_principal_name: Optional[str] = None
    ) -> Union[User, None]:
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
            Union[User, None]:
                A User object if the user is found, None otherwise.
        
        Raises
            ValueError:
                Raises this error if neither argument is provided
        """

        if user_id:
            # Build endpoint and URL
            user_fetch_endpoint = self._endpoints[self.GET_USER].format(id=user_id)
            graph_api_url = self.build_url(user_fetch_endpoint)
        elif user_principal_name:
            # Build endpoint and URL
            user_fetch_endpoint = self._endpoints[self.GET_USER].format(id=user_principal_name)
            graph_api_url = self.build_url(user_fetch_endpoint)
        else:
            raise ValueError('Either a user_id or a user_principal_name must'
                                + ' be provided.')

        # Make API call
        response = self.graph_connector.get(graph_api_url)
        if not response.status_code == HTTPStatus.OK: # Checking for 200
            logger.error('Error when getting user from Graph API')
            logger.error(response.content)
            return None
        
        user_json = response.json()
        new_user = User(self.graph_connector, user_json)
        
        return new_user
    
    def create_user(self, user_data: dict) -> Union[User, None]:
        """
        Creates a user in the Microsoft organization

        Parameters
            user_data : dict
                dictionary representing user data to be POST'd to Microsoft. The
                required fields can be found in the example below
        
        Returns
            Union[User, None]:
                Returns a User object representing the new User created, or None if
                the User could not be created
        
        Raises
            ValueError:
                Raises if required fields aren't all present in user_data
        
        Usage
            example dictionary with required fields:
            {
                "accountEnabled": true,
                "displayName": "Adele Vance",
                "mailNickname": "AdeleV",
                "userPrincipalName": "AdeleV@contoso.onmicrosoft.com",
                "passwordProfile" : {
                    "forceChangePasswordNextSignIn": true,
                    "password": "xWwvJ]6NMw+bWH-d"
                }
            }
            Additional information can be found in the Graph API docs for Users
            and Create User, as well as our documentation
        """

        # Checking if required data is in provided JSON for POST
        required_keys = ['accountEnabled', 'displayName', 'mailNickname',
                        'userPrincipalName', 'passwordProfile']
        for key in required_keys:
            if key not in user_data:
                raise ValueError(f'Key "{key}" is required and was not provided'
                                + ' in the user_data parameter')
        
        # Build URL for HTTP request
        graph_api_url = self.build_url(self._endpoints[self.CREATE_USER])

        # Make POST request
        response = self.graph_connector.post(graph_api_url, user_data)
        if not response.status_code == HTTPStatus.CREATED: # Checking for 201
            logger.error('Error when creating user in Graph API')
            logger.error(response.content)
            return None
        
        user_json = response.json()
        new_user = User(self.graph_connector, user_json)
        
        return new_user