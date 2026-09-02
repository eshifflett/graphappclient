from unittest.mock import patch
import pytest
from graphappclient.api_connector import APIConnector
from graphappclient.constants import ACCESS_TOKEN, DEFAULT_SCOPE

# pytest fixture for mocking an APIConnector's MSAL object to avoid API calls while testing
# yields a tuple containing (APIConnector, Mocked_MSAL_Object)
@pytest.fixture
def connector():
    with patch(
        "graphappclient.api_connector.ConfidentialClientApplication"
    ) as mock_msal:
        connector = APIConnector(
            "client-id",
            "tenant-id",
            "client-secret"
        )
        yield connector, mock_msal.return_value

# Testing getting access token from cache
def test_get_token_from_cache(connector):
    # unpacks APIConnector object, and associated mocked MSAL object
    api_connector, mock_msal = connector

    # fake token to return
    fake_token = "fake-token"

    # mocking return value of MSAL acquire_token_silent to return token with no API call
    mock_msal.acquire_token_silent.return_value = {
        ACCESS_TOKEN: fake_token
    }

    # requesting token from APIConnector
    result = api_connector._get_token()

    # Assertions
    assert result == fake_token # token found
    mock_msal.acquire_token_silent.assert_called_once_with( # cache check called once
        DEFAULT_SCOPE,
        None
    )
    mock_msal.acquire_token_for_client.assert_not_called() # no API call made

# Testing requesting access token from API when none is cached
def test_get_token_from_microsoft_when_cache_empty(connector):
    # unpacks APIConnector object, and associated mocked MSAL object
    api_connector, mock_msal = connector

    # fake token to return
    fake_token = "fake-token"

    # mocking cache check failure, and API call success
    mock_msal.acquire_token_silent.return_value = None
    mock_msal.acquire_token_for_client.return_value = {
        ACCESS_TOKEN: fake_token
    }

    # attempting to get token with APIConnector
    result = api_connector._get_token()

    # Assertions
    assert result == fake_token # Assert token fetched and correctly saved in connector object
    mock_msal.acquire_token_silent.assert_called_once_with( # Assert ConfidentialClientApplication.acquire_token_silent() was called exactly once
        DEFAULT_SCOPE,
        None
    )
    mock_msal.acquire_token_for_client.assert_called_once_with( # Assert ConfidentialClientApplication.acquire_token_for_client() was called exactly once
        scopes=DEFAULT_SCOPE
    )

# Testing cache failing AND Microsoft API failing
def test_get_token_failure(connector):
    api_connector, mock_msal = connector

    mock_msal.acquire_token_silent.return_value = None
    mock_msal.acquire_token_for_client.return_value = None

    # Failing get_token
    result = api_connector._get_token()

    assert result is None
    mock_msal.acquire_token_silent.assert_called_once_with(
        DEFAULT_SCOPE,
        None
    )
    mock_msal.acquire_token_for_client.assert_called_once_with(
        scopes=DEFAULT_SCOPE
    )

# Testing behavior when authentication successful
@patch.object(APIConnector, "_get_token")
def test_authenticate_success(mock_get_token, connector):
    # unpacks APIConnector object, and associated mocked MSAL object
    api_connector, _ = connector
    
    # fake token to return
    fake_token = "fake-token"

    # Setting APIConnector._get_token() return value to return a valid token
    mock_get_token.return_value = fake_token

    # calling authenticate function
    result = api_connector.authenticate()

    assert result is True # asserting that authenticate() returns true when successfully acquiring token
    mock_get_token.assert_called_once() # asserting that APIConnector._get_token() is called only once

# Testing behavior when authentication failure
@patch.object(APIConnector, "_get_token")
def test_authenticate_failure(mock_get_token, connector):
    # unpacks APIConnector object, and associated mocked MSAL object
    api_connector, _ = connector

    # Setting APIConnector._get_token() return value to None to reflect no token acquired
    mock_get_token.return_value = None

    # calling authenticate function
    result = api_connector.authenticate()

    assert result is False # asserting that authenticate() returns false when successfully acquiring token
    mock_get_token.assert_called_once() # asserting that APIConnector._get_token() is called only once

# Testing that headers object is successfully created with token
@patch.object(APIConnector, "_get_token")
def test_get_headers(mock_get_token, connector):
    # unpacks APIConnector object, and associated mocked MSAL object
    api_connector, mock_msal = connector
    
    # fake token to return
    fake_token = "fake-token"

    # Setting APIConnector._get_token() return value to return a valid token
    mock_get_token.return_value = fake_token

    # getting the headers
    result = api_connector._get_headers()

    mock_get_token.assert_called_once()
    assert result == {'Authorization': 'Bearer ' + fake_token} # asserting that the result is our headers object with the appropriate token

# Testing the HTTP get request is correctly constructed and response received
@patch.object(APIConnector, "_get_headers")
@patch("graphappclient.api_connector.requests.get")
def test_get(mock_get, mock_get_headers, connector):
    # unpacks APIConnector object, and associated mocked MSAL object
    api_connector, _ = connector

    # Example get parameters
    url = "https://example.com"

    # headers
    headers = {"Authorization": "Bearer fake-token"}
    mock_get_headers.return_value = headers

    # Act
    response = api_connector.get(url)
    fake_http_response = mock_get.return_value

    # Assert
    mock_get_headers.assert_called_once()
    mock_get.assert_called_once_with(
        url,
        headers=headers
    )
    assert response == fake_http_response

# Testing the HTTP post request is correctly constructed and response received
@patch.object(APIConnector, "_get_headers")
@patch("graphappclient.api_connector.requests.post")
def test_post(mock_post, mock_get_headers, connector):
    # unpacks APIConnector object, and associated mocked MSAL object
    api_connector, _ = connector

    # Example post parameters
    url = "https://example.com"
    json = {"name": "Ethan"}

    # Fake headers
    headers = {"Authorization": "Bearer fake-token"}
    mock_get_headers.return_value = headers

    # Act
    response = api_connector.post(url, json)
    fake_http_response = mock_post.return_value

    # Assert
    mock_get_headers.assert_called_once()
    mock_post.assert_called_once_with(
        url,
        json=json,
        headers=headers
    )
    assert response == fake_http_response

# Testing the HTTP delete request is correctly constructed and response received
@patch.object(APIConnector, "_get_headers")
@patch("graphappclient.api_connector.requests.delete")
def test_delete(mock_delete, mock_get_headers, connector):
    # unpacks APIConnector object, and associated mocked MSAL object
    api_connector, _ = connector

    # Example post parameters
    url = "https://example.com"
    json = {"name": "Ethan"}

    # Fake headers
    headers = {"Authorization": "Bearer fake-token"}
    mock_get_headers.return_value = headers

    # Act
    response = api_connector.delete(url, json)
    fake_http_response = mock_delete.return_value

    # Assert
    mock_get_headers.assert_called_once()
    mock_delete.assert_called_once_with(
        url,
        json=json,
        headers=headers
    )
    assert response == fake_http_response

# Testing the HTTP patch request is correctly constructed and response received
@patch.object(APIConnector, "_get_headers")
@patch("graphappclient.api_connector.requests.patch")
def test_patch(mock_patch, mock_get_headers, connector):
    # unpacks APIConnector object, and associated mocked MSAL object
    api_connector, _ = connector

    # Example post parameters
    url = "https://example.com"
    json = {"name": "Ethan"}

    # Fake headers
    headers = {"Authorization": "Bearer fake-token"}
    mock_get_headers.return_value = headers

    # Act
    response = api_connector.patch(url, json)
    fake_http_response = mock_patch.return_value

    # Assert
    mock_get_headers.assert_called_once()
    mock_patch.assert_called_once_with(
        url,
        json=json,
        headers=headers
    )
    assert response == fake_http_response