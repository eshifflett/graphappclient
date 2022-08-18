CLIENT_ID = 'f88cc666-d80b-43ec-9447-9d5ade2b4916'
TENANT_ID = '8af89135-934b-42e9-aee7-29fd57dee1bd'
CLIENT_SECRET = '4KD8Q~_egEv1O1pslpRPp6QwLu6J-XYVdLTRMdoR'
LOGIN_AUTH_URL = 'https://login.microsoftonline.com/'
DEFAULT_SCOPE = ['https://graph.microsoft.com/.default']

import graphclient

graphapp = graphclient.GraphAppClient(CLIENT_ID, TENANT_ID, CLIENT_SECRET)
print("Authentication attempt result: " + graphapp.authenticate().__str__())
# print(graphapp._access_token)

users = graphapp.get_users()
print('Users fetched:')
print(users)

print('Fetching Adele:')
from_new = graphapp.get_user(user_principal_name='AdeleV@4rlq7s.onmicrosoft.com')

print(from_new)