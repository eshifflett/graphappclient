from unittest.mock import patch

from graphappclient.api_connector import APIConnector
from graphappclient.constants import ACCESS_TOKEN, DEFAULT_SCOPE


@patch("graphappclient.api_connector.ConfidentialClientApplication") # replace CCA with mock object to avoid real API calls
def test_get_token_from_cache(mock_msal):

    #
    # ARRANGE
    #
    # Mock return of cached token using mock_msal object
    fake_token = "fake-token"
    mock_msal_instance = mock_msal.return_value
    mock_msal_instance.acquire_token_silent.return_value = {
        ACCESS_TOKEN: fake_token
    }

    # Now that mocking is done, let's create our API connector to test
    connector = APIConnector(
        "client-id",
        "tenant-id",
        "client-secret"
    )

    #
    # ACT
    #
    # Attempting to get token from cache
    result = connector._get_token()

    #
    # ASSERT
    #
    # Assert we received the correct token
    assert result == fake_token

    # Assert APIConnector.acquire_token_silent() was called exactly once
    mock_msal_instance.acquire_token_silent.assert_called_once_with(
        DEFAULT_SCOPE,
        None
    )

    # Assert APIConnector.acquire_token_for_client() was not called
    # meaning no token was requested from Microsoft
    mock_msal_instance.acquire_token_for_client.assert_not_called()