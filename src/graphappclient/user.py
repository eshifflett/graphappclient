from graphappclient.api_connector import APIConnector
from graphappclient.constants import (BUSINESS_PHONES, DISPLAY_NAME, GIVEN_NAME, ID,
                                    JOB_TITLE, MAIL, MOBILE_PHONE, OFFICE_LOCATION,
                                    PREFERRED_LANGUAGE, SURNAME, USER_PRINCIPAL_NAME,
                                    VALUE)
from graphappclient.utils import APIBase
from http import HTTPStatus
import logging
from typing import List

# Logger
logger = logging.getLogger(__name__)

class User(APIBase):
    """
    Class representing a user object for Microsoft. More info found here:
    https://docs.microsoft.com/en-us/graph/api/resources/user
    """

    DELETE_USER = 'delete_user'

    _endpoints = {
        DELETE_USER : '/users/{id}'
    }

    def __init__(self, api_connector: APIConnector, user_json: dict):
        """
        """

        # Super class constructor
        super().__init__()

        self.graph_connector = api_connector
        self.business_phones = user_json.get(BUSINESS_PHONES)
        self.display_name = user_json.get(DISPLAY_NAME)
        self.given_name = user_json.get(GIVEN_NAME)
        self.job_title = user_json.get(JOB_TITLE)
        self.mail = user_json.get(MAIL)
        self.mobile_phone = user_json.get(MOBILE_PHONE)
        self.office_location = user_json.get(OFFICE_LOCATION)
        self.preferred_language = user_json.get(PREFERRED_LANGUAGE)
        self.surname = user_json.get(SURNAME)
        self.user_principal_name = user_json.get(USER_PRINCIPAL_NAME)
        self.id = user_json.get(ID)
    
    def __repr__(self):
        return f'User {self.user_principal_name} with ID {self.id}'
    
    def delete_user(self) -> bool:
        # Build endpoint and URL
        user_fetch_endpoint = self._endpoints[self.DELETE_USER].format(id=self.id)
        graph_api_url = self.build_url(user_fetch_endpoint)

        # Make API call
        response = self.graph_connector.delete(graph_api_url)
        if not response.status_code == HTTPStatus.NO_CONTENT: # Checking for 200
            logger.error('Error when getting user from Graph API')
            logger.error(response.content)
            return False
        
        return True