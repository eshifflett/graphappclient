# URL for authentication with MSAL
LOGIN_AUTH_URL = 'https://login.microsoftonline.com/'

# Graph API base URL and version
GRAPH_BASE_URL = 'https://graph.microsoft.com/'
API_VERSION = 'v1.0'

# Default scope required for application permissions
DEFAULT_SCOPE = ['https://graph.microsoft.com/.default']

# Misc dict keys
ERROR = 'error'
ACCESS_TOKEN = 'access_token'
VALUE = 'value'
NEXT_ODATA = '@odata.nextLink'

# Query Param Strings
TOP_QUERY = '$top='



################################################################################
# USER OBJECT CONSTANTS
################################################################################
BUSINESS_PHONES = 'businessPhones'
DISPLAY_NAME = 'displayName'
GIVEN_NAME = 'givenName'
JOB_TITLE = 'jobTitle'
MAIL = 'mail'
MOBILE_PHONE = 'mobilePhone'
OFFICE_LOCATION = 'officeLocation'
PREFERRED_LANGUAGE = 'preferredLanguage'
SURNAME = 'surname'
USER_PRINCIPAL_NAME = 'userPrincipalName'
USER_ID = 'id'
DEFAULT_USER_SELECT = f'$select={BUSINESS_PHONES},{DISPLAY_NAME},{GIVEN_NAME},{JOB_TITLE},{MAIL},{MOBILE_PHONE},{OFFICE_LOCATION},{PREFERRED_LANGUAGE},{SURNAME},{USER_PRINCIPAL_NAME},{USER_ID}'