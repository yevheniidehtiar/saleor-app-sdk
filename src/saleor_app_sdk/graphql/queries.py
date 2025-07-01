"""
Pre-built GraphQL queries for common operations
"""

from gql import gql


class SaleorQueries:
    """Pre-built GraphQL queries for common operations"""

    APP_INFO = gql("""
        query GetApp {
            app {
                id
                name
                isActive
                permissions {
                    code
                    name
                }
            }
        }
    """)

    ORDERS_LIST = gql("""
        query GetOrders($first: Int!, $after: String) {
            orders(first: $first, after: $after) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                edges {
                    node {
                        id
                        number
                        status
                        total {
                            gross {
                                amount
                                currency
                            }
                        }
                        user {
                            email
                            firstName
                            lastName
                        }
                        created
                        updatedAt
                    }
                }
            }
        }
    """)

    PRODUCT_LIST = gql("""
        query GetProducts($first: Int!, $after: String) {
            products(first: $first, after: $after) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                edges {
                    node {
                        id
                        name
                        slug
                        description
                        category {
                            name
                        }
                        defaultVariant {
                            pricing {
                                price {
                                    gross {
                                        amount
                                        currency
                                    }
                                }
                            }
                        }
                        created
                        updatedAt
                    }
                }
            }
        }
    """)
