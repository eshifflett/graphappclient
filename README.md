# graphappclient - A Backend Microsoft Graph API Application Client
This library aims to provide simple, easy to understand support for interaction with Microsoft's Graph API components for backend applications [that authenticate with their own identity.](https://docs.microsoft.com/en-us/graph/auth-v2-service) Currently provides full support for Graph API interaction with Users, and the immediate future plans are adding support for OneDrive and SharePoint.

This project is primarily developed and maintained by [eshifflett](https://github.com/eshifflett).

## Quick Code Example:
```python
from graphappclient.graphclient import GraphAppClient

# These will need to contain actual values
CLIENT_ID = '<Client ID>'
TENANT_ID = '<Tenant ID>'
CLIENT_SECRET = '<Client Secret>'

# Create client and authenticate
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

## Authentication and Permissions
Before interaction with the Microsoft Graph API can be done with this library, an initial setup must be performed by an administrator of your Microsoft Organization. For more details about the authentication process and requesting the necessary permissions to perform your wanted actions, [view our documentation on the process here]().

## Graph API Components
### Users
Users are accessed and interacted with via the `GraphAppClient` and `User` classes.
#### Get Users
```python
GraphAppClient.get_users(self, page_size: int = None, limit: int = None) -> Union[List[User], Paginator, None]
```

Gets a collection of `User` objects. Users can specify a `page_size` to request specifically sized batches of responses, and a `limit` to set a cap on the number of objects returned. If a `page_size` is supplied and there is a greater amount of data returned, the function will return a `Pagination` object as opposed to a `List[User]`. `Pagination` is a custom data structure that supports iteration and requests the data in batches. Some requests have default maximum page sizes in the Graph API as well, more can be read in our documentation on the structure.

```python
GraphAppClient.get_user(self, user_id: Optional[str] = None, user_principal_name: Optional[str] = None) -> Union[User, None]
```
This will get an individual `User` object, either from a provided `user_id` or `user_principal_name`. It will prioritize fetching from the `user_id` parameter over the `user_principal_name`, only one should be provided. In practice, the `user_principal_name` will probably be used most (it is equivalent to the user's login name, such as 'AdeleV@contoso.onmicrosoft.com'.

#### Create Users
```python
GraphAppClient.create_user(self, user_data: dict) -> Union[User, None]
```
This is used to create a User in the Microsoft organization, and returns a `User` object representing the newly created User. The user is created from information provided in the `user_data` dictionary, which should match the [JSON representation of User objects in the Graph API documentation](https://docs.microsoft.com/en-us/graph/api/user-post-users?view=graph-rest-1.0&tabs=http#request-body).

#### Edit/Update Users
```python
User.update_user(self, updates: Optional[dict] = None, include_attributes: Optional[bool] = False) -> bool
```
Used to edit fields of the User object in Microsoft. There are two ways of specifying the updates to the organization. First, a [dictionary representing a JSON object of User key/values](https://docs.microsoft.com/en-us/graph/api/user-update?view=graph-rest-1.0&tabs=http#request-body) can be provided as the `updates` parameter. Any updates passed this way are also added to the `user_json` field of the `User` object after `update_user()` is called. Second, any of the attributes of the `User` object can be edited like normal class attributes, and will be included in the update if the `include_attributes` parameter is set to `True`. It will return a `bool` value indicating whether or not the update was successful.

#### Delete Users
```python
User.delete_user(self) -> bool
```
Finally, this function is used to delete Users from their Microsoft organization. It returns a `bool` indicating whether or not the deletion operation was successful. It should be noted that after this is executed, other functioniality of this `User` object is (obviously) lost. 

## Other Library Infrastructure
### Paginator
The `Paginator` class is a custom data structure that is used for storying results of queries that return more than one page of data. Various functions in this library have `page_size` parameters, and the Graph API also has some default page size maximums for some of their queries. This data structure is iterable and will continuously request data as the previous page runs out until no more data is sent from Microsoft. In addition to iterating over the whole collection, you can also access the `page` attribute of the object itself to just get the current page as a `List`, and call `Paginator.next_page()` to receive the next page of data from Microsoft.
#### Code Example
```python
from graphappclient.graphclient import GraphAppClient

# These will need to contain actual values
CLIENT_ID = '<Client ID>'
TENANT_ID = '<Tenant ID>'
CLIENT_SECRET = '<Client Secret>'

# Create client and authenticate
client = GraphAppClient(CLIENT_ID, TENANT_ID, CLIENT_SECRET)
client.authenticate()

# Iterating directly
# Get 100 users, page_size = 20, will come as a Paginator in 5 pages
users = client.get_users(page_size=20, limit=100)
for user in users: # Will print all 100 users, automatically requests more every 20
  print(user)

# Iterating page by page
# Get 100 users, page_size = 20, will come as a Paginator in 5 pages
users = client.get_users(page_size=20, limit=100)
for user in users.page # Iterate over first page, 20 Users
  print(user)

users.next_page() # Requests next page of data from Microsoft and updates data structure
for user in users.page # Iterate over second page, 20 more users
  print(user)
```
