from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from saleor_app_sdk.graphql.client import SaleorGraphQLClient


class TestSaleorGraphQLClient:
    def test_init(self, auth_token, saleor_api_url):
        """Test initialization of SaleorGraphQLClient"""
        client = SaleorGraphQLClient(api_url=saleor_api_url, auth_token=auth_token)

        assert client.api_url == saleor_api_url
        assert client.auth_token == auth_token
        assert client._client is None

    def test_client_property(
        self, auth_token, saleor_api_url, mock_httpx_transport, mock_gql_client
    ):
        """Test client property creates a GQL client with correct configuration"""
        with patch(
            "saleor_app_sdk.graphql.client.Client", return_value=mock_gql_client
        ) as mock_client_class:
            client = SaleorGraphQLClient(api_url=saleor_api_url, auth_token=auth_token)

            # Access the client property to trigger client creation
            gql_client = client.client

            # Verify HTTPXTransport was created with correct parameters
            mock_httpx_transport.assert_called_once_with(
                url=saleor_api_url, headers={"Authorization": f"Bearer {auth_token}"}
            )

            # Verify Client was created with correct parameters
            mock_client_class.assert_called_once()
            assert gql_client is mock_gql_client

            # Verify client is cached
            assert client._client is mock_gql_client

            # Access the client property again
            gql_client2 = client.client

            # Verify no new client was created
            assert mock_client_class.call_count == 1
            assert gql_client2 is mock_gql_client

    def test_execute(self, auth_token, saleor_api_url):
        """Test execute method"""
        # Create a mock GQL client
        mock_client = MagicMock()
        mock_client.execute.return_value = {"data": {"test": "value"}}

        # Create a client with the mock GQL client
        client = SaleorGraphQLClient(api_url=saleor_api_url, auth_token=auth_token)
        client._client = mock_client

        # Execute a query
        query = "query { test }"
        variables = {"var": "value"}

        import asyncio

        result = asyncio.run(client.execute(query, variables))

        # Verify the query was executed with correct parameters
        mock_client.execute.assert_called_once_with(query, variable_values=variables)
        assert result == {"data": {"test": "value"}}

    def test_execute_without_variables(self, auth_token, saleor_api_url):
        """Test execute method without variables"""
        # Create a mock GQL client
        mock_client = MagicMock()
        mock_client.execute.return_value = {"data": {"test": "value"}}

        # Create a client with the mock GQL client
        client = SaleorGraphQLClient(api_url=saleor_api_url, auth_token=auth_token)
        client._client = mock_client

        # Execute a query without variables
        query = "query { test }"

        import asyncio

        result = asyncio.run(client.execute(query))

        # Verify the query was executed with empty variables
        mock_client.execute.assert_called_once_with(query, variable_values={})
        assert result == {"data": {"test": "value"}}

    def test_execute_error(self, auth_token, saleor_api_url):
        """Test execute method with error"""
        # Create a mock GQL client that raises an exception
        mock_client = MagicMock()
        mock_client.execute.side_effect = Exception("GraphQL error")

        # Create a client with the mock GQL client
        client = SaleorGraphQLClient(api_url=saleor_api_url, auth_token=auth_token)
        client._client = mock_client

        # Execute a query
        query = "query { test }"

        import asyncio

        with pytest.raises(Exception, match="GraphQL error"):
            asyncio.run(client.execute(query))

        # Verify the query was executed
        mock_client.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_async(self, auth_token, saleor_api_url):
        """Test execute_async method"""
        # Create a mock GQL client with async context manager
        mock_session = AsyncMock()
        mock_session.execute.return_value = {"data": {"test": "value"}}

        mock_client = MagicMock()
        mock_client.__aenter__.return_value = mock_session

        # Create a client with the mock GQL client
        client = SaleorGraphQLClient(api_url=saleor_api_url, auth_token=auth_token)
        client._client = mock_client

        # Execute a query asynchronously
        query = "query { test }"
        variables = {"var": "value"}

        result = await client.execute_async(query, variables)

        # Verify the query was executed with correct parameters
        mock_session.execute.assert_called_once_with(query, variable_values=variables)
        assert result == {"data": {"test": "value"}}

    @pytest.mark.asyncio
    async def test_execute_async_without_variables(self, auth_token, saleor_api_url):
        """Test execute_async method without variables"""
        # Create a mock GQL client with async context manager
        mock_session = AsyncMock()
        mock_session.execute.return_value = {"data": {"test": "value"}}

        mock_client = MagicMock()
        mock_client.__aenter__.return_value = mock_session

        # Create a client with the mock GQL client
        client = SaleorGraphQLClient(api_url=saleor_api_url, auth_token=auth_token)
        client._client = mock_client

        # Execute a query asynchronously without variables
        query = "query { test }"

        result = await client.execute_async(query)

        # Verify the query was executed with empty variables
        mock_session.execute.assert_called_once_with(query, variable_values={})
        assert result == {"data": {"test": "value"}}
