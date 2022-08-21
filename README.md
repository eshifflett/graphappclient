# graphappclient - A Backend Microsoft Graph API Application Client
This library aims to provide simple, easy to understand support for interaction with Microsoft's Graph API components for backend applications [that authenticate with their own identity.](https://docs.microsoft.com/en-us/graph/auth-v2-service) Currently provides full support for Graph API interaction with Users, and the immediate future plans are adding support for OneDrive and SharePoint.

This project is primarily developed and maintained by [eshifflett](https://github.com/eshifflett).

### Quick Code Example:
```python
from graphappclient.graphclient import GraphAppClient

CLIENT_ID = '<Client ID>'
TENANT_ID = '<Tenant ID>'
CLIENT_SECRET = '<Client Secret>'

client = GraphAppClient(CLIENT_ID, TENANT_ID, CLIENT_SECRET)
client.authenticate()

# Get 100 users
users = client.get_users(limit=100)
selected_user = users[0]

# Update user
selected_user.job_title = 'Sr. Software Engineer'
updates = {"city" : "New York City"}
selected_user.update_user(updates=updates, include_attributes=True)

# Delete user
selected_user.delete_user()
```

## Graph API Components
### Users
Users are accessed and interacted with via the `GraphAppClient` and `User` classes.
#### Get Users
```python
GraphAppClient.get_users(self, page_size: int = None, limit: int = None) -> Union[List[User], Paginator, None]
```

Gets a collection of `User` objects. Users can specify a `page_size` to request specifically sized batches of responses, and a `limit` to set a cap on the number of objects returned. If a `page_size` is supplied and there is a greater amount of data returned, the function will return a `Pagination` object as opposed to a `List[User]`. `Pagination` is a custom data structure that supports iteration and requests the data in batches of size `page_size`, more can be read in our documentation on the structure.

