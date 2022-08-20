from graphappclient.api_connector import APIConnector
from graphappclient.constants import (BUSINESS_PHONES, DISPLAY_NAME, GIVEN_NAME, ID,
                                    JOB_TITLE, MAIL, MOBILE_PHONE, OFFICE_LOCATION,
                                    PREFERRED_LANGUAGE, SURNAME, USER_PRINCIPAL_NAME,
                                    VALUE)
from graphappclient.utils import APIBase
from typing import List

class User(APIBase):
    """
    Class representing a user object for Microsoft. More info found here:
    https://docs.microsoft.com/en-us/graph/api/resources/user
    """

    def __init__(self, api_connector: APIConnector, user_json: dict):
        """
        """
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