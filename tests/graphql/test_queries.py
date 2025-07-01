import pytest
from gql import gql

from saleor_app_sdk.graphql.queries import SaleorQueries


class TestSaleorQueries:
    def test_app_info_query(self):
        """Test APP_INFO query"""
        query = SaleorQueries.APP_INFO

        # Verify it's a gql object (DocumentNode)
        assert hasattr(query, 'loc')

        # We can't easily check the content of the query from the DocumentNode object
        # Just verify it's not None
        assert query is not None

    def test_orders_list_query(self):
        """Test ORDERS_LIST query"""
        query = SaleorQueries.ORDERS_LIST

        # Verify it's a gql object (DocumentNode)
        assert hasattr(query, 'loc')

        # We can't easily check the content of the query from the DocumentNode object
        # Just verify it's not None
        assert query is not None

    def test_product_list_query(self):
        """Test PRODUCT_LIST query"""
        query = SaleorQueries.PRODUCT_LIST

        # Verify it's a gql object (DocumentNode)
        assert hasattr(query, 'loc')

        # We can't easily check the content of the query from the DocumentNode object
        # Just verify it's not None
        assert query is not None

    def test_query_execution(self, mock_gql_client):
        """Test executing queries with a GraphQL client"""
        from saleor_app_sdk.graphql.client import SaleorGraphQLClient

        # Create a client with the mock GQL client
        client = SaleorGraphQLClient(api_url="https://example.com/graphql", auth_token="token")
        client._client = mock_gql_client

        # Execute each query
        import asyncio

        # APP_INFO query
        asyncio.run(client.execute(SaleorQueries.APP_INFO))
        mock_gql_client.execute.assert_called_with(SaleorQueries.APP_INFO, variable_values={})
        mock_gql_client.reset_mock()

        # ORDERS_LIST query with variables
        variables = {"first": 10, "after": None}
        asyncio.run(client.execute(SaleorQueries.ORDERS_LIST, variables))
        mock_gql_client.execute.assert_called_with(SaleorQueries.ORDERS_LIST, variable_values=variables)
        mock_gql_client.reset_mock()

        # PRODUCT_LIST query with variables
        variables = {"first": 10, "after": None}
        asyncio.run(client.execute(SaleorQueries.PRODUCT_LIST, variables))
        mock_gql_client.execute.assert_called_with(SaleorQueries.PRODUCT_LIST, variable_values=variables)
