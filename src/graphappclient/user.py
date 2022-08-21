from unittest.mock import patch
from graphappclient.api_connector import APIConnector
from graphappclient.constants import (BUSINESS_PHONES, DISPLAY_NAME, GIVEN_NAME, ID,
                                    JOB_TITLE, MAIL, MOBILE_PHONE, OFFICE_LOCATION,
                                    PREFERRED_LANGUAGE, SURNAME, USER_PRINCIPAL_NAME,
                                    VALUE)
from graphappclient.utils import APIBase
from http import HTTPStatus
import logging
from typing import List, Optional

# Logger
logger = logging.getLogger(__name__)

class User(APIBase):
    """
    Class representing a user object for Microsoft. More info found here:
    https://docs.microsoft.com/en-us/graph/api/resources/user
    """

    DELETE_USER = 'delete_user'
    UPDATE_USER = 'update_user'

    _endpoints = {
        DELETE_USER : '/users/{id}',
        UPDATE_USER : '/users/{id}'
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
        self.user_json = user_json
    
    def __repr__(self):
        return f'User {self.user_principal_name} with ID {self.id}'
    
    def delete_user(self) -> bool:
        # Build endpoint and URL
        user_fetch_endpoint = self._endpoints[self.DELETE_USER].format(id=self.id)
        graph_api_url = self.build_url(user_fetch_endpoint)

        # Make API call
        response = self.graph_connector.delete(graph_api_url)
        if not response.status_code == HTTPStatus.NO_CONTENT: # Checking for 204
            logger.error('Error when getting user from Graph API')
            logger.error(response.content)
            return False
        
        return True
    
    def update_user(self, updates: Optional[dict] = None, include_attributes: Optional[bool] = False) -> bool:
        """"""

        # Input validation
        if updates == None and not include_attributes:
            raise ValueError('Must either provide updates JSON or request to'
            + ' include_attributes in update, or both')

        # Adding updates to user_json
        if updates:
            for key in updates:
                self.user_json[key] = updates[key]

        # Updating potential attribute changes to self.user_json
        if include_attributes:
            self.user_json[BUSINESS_PHONES] = self.business_phones
            self.user_json[DISPLAY_NAME] = self.display_name
            self.user_json[GIVEN_NAME] = self.given_name
            self.user_json[JOB_TITLE] = self.job_title
            self.user_json[MAIL] = self.mail
            self.user_json[MOBILE_PHONE] = self.mobile_phone
            self.user_json[OFFICE_LOCATION] = self.office_location
            self.user_json[PREFERRED_LANGUAGE] = self.preferred_language
            self.user_json[SURNAME] = self.surname
            self.user_json[USER_PRINCIPAL_NAME] = self.user_principal_name
            self.user_json[ID] = self.id
        
        # Getting JSON to patch to MS
        patch_json = self.user_json if include_attributes else updates

        # Build endpoint and URL
        user_fetch_endpoint = self._endpoints[self.UPDATE_USER].format(id=self.id)
        graph_api_url = self.build_url(user_fetch_endpoint)

        # Make API call
        response = self.graph_connector.patch(graph_api_url, json=patch_json)
        if not response.status_code == HTTPStatus.NO_CONTENT: # Checking for 204
            logger.error('Error when updating user via Graph API')
            logger.error(response.content)
            return False
        
        return True
