import api_connector
from typing import List
from utils import APIBase

class User(APIBase):
    """
    Class representing a user object for Microsoft. More info found here:
    https://docs.microsoft.com/en-us/graph/api/resources/user
    """

    def __init__(
        self,
        api_connector: api_connector.APIConnector,
        business_phones: List[str],
        display_name: str,
        given_name: str,
        job_title: str,
        mail: str,
        mobile_phone: str,
        office_location: str,
        preferred_language: str,
        surname: str,
        user_principal_name: str,
        id: str
    ):
        """
        """
        self.api_connector = api_connector
        self.business_phones = business_phones
        self.display_name = display_name
        self.given_name = given_name
        self.job_title = job_title
        self.mail = mail
        self.mobile_phone = mobile_phone
        self.office_location = office_location
        self.preferred_language = preferred_language
        self.surname = surname
        self.user_principal_name = user_principal_name
        self.id = id
    
    def __repr__(self):
        return f'User {self.user_principal_name} with ID {self.id}'