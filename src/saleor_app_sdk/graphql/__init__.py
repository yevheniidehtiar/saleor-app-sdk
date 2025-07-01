"""
GraphQL-related functionality for Saleor App SDK
"""

from .client import SaleorGraphQLClient
from .queries import SaleorQueries

__all__ = ["SaleorGraphQLClient", "SaleorQueries"]
