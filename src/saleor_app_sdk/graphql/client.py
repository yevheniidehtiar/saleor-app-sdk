"""
GraphQL client for Saleor API
"""

import logging

from gql import Client
from gql.transport.httpx import HTTPXTransport

logger = logging.getLogger(__name__)


class SaleorGraphQLClient:
    """Enhanced GraphQL client for Saleor API"""

    def __init__(self, api_url: str, auth_token: str):
        self.api_url = api_url
        self.auth_token = auth_token
        self._client = None

    @property
    def client(self) -> Client:
        if self._client is None:
            transport = HTTPXTransport(
                url=self.api_url, headers={"Authorization": f"Bearer {self.auth_token}"}
            )
            self._client = Client(transport=transport, fetch_schema_from_transport=True)
        return self._client

    async def execute(self, query, variables: dict | None = None):
        """Execute GraphQL query/mutation"""
        try:
            return self.client.execute(query, variable_values=variables or {})
        except Exception:
            logger.exception("GraphQL execution failed")
            raise

    async def execute_async(self, query, variables: dict | None = None):
        """Execute GraphQL query/mutation asynchronously"""
        async with self.client as session:
            return await session.execute(query, variable_values=variables or {})
