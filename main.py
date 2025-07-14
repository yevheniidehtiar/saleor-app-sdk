import logging
import os
from typing import List, Optional

from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from gql import gql

from saleor_app_sdk import SaleorAppBuilder, SaleorPermission, WebhookEventType
from saleor_app_sdk.graphql.queries import SaleorQueries

# Create your Saleor app
saleor_app = (
    SaleorAppBuilder("saleor-app", "Saleor App")
    .version("0.1.0")
    .about("A Saleor app built with saleor-app-sdk")
    .permissions(SaleorPermission.MANAGE_ORDERS, SaleorPermission.MANAGE_PRODUCTS)
    .urls(
        app_url=os.environ.get("APP_URL", "http://localhost:8000"),
        config_url=os.environ.get("CONFIG_URL", "http://localhost:8000/config"),
    )
    .secret_key(
        os.environ.get("SECRET_KEY", "your-secret-key")
    )  # Change this in production!
    .base_url(os.environ.get("BASE_URL", "http://localhost:8000"))
    .build()
)

# Export the FastAPI app as the main app for Uvicorn
app = saleor_app.fastapi_app
logger = logging.getLogger(__name__)

# Define additional GraphQL queries for product operations
PRODUCT_SEARCH_QUERY = gql("""
    query SearchProducts($search: String!, $first: Int!) {
        products(filter: {search: $search}, first: $first) {
            edges {
                node {
                    id
                    name
                    description
                    isPublished
                    pricing {
                        priceRange {
                            start {
                                gross {
                                    amount
                                    currency
                                }
                            }
                        }
                    }
                }
            }
        }
    }
""")

PRODUCT_DETAILS_QUERY = gql("""
    query GetProduct($id: ID!) {
        product(id: $id) {
            id
            name
            description
            isPublished
            pricing {
                priceRange {
                    start {
                        gross {
                            amount
                            currency
                        }
                    }
                }
            }
        }
    }
""")

CREATE_PRODUCT_MUTATION = gql("""
    mutation CreateProduct($input: ProductCreateInput!) {
        productCreate(input: $input) {
            product {
                id
                name
            }
            errors {
                field
                message
            }
        }
    }
""")

DELETE_PRODUCT_MUTATION = gql("""
    mutation DeleteProduct($id: ID!) {
        productDelete(id: $id) {
            product {
                id
            }
            errors {
                field
                message
            }
        }
    }
""")


@saleor_app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return saleor_app.templates.TemplateResponse("index.html", {"request": request})


@saleor_app.get("/products", response_class=HTMLResponse)
async def products_page(request: Request):
    return saleor_app.templates.TemplateResponse("products.html", {"request": request})


@saleor_app.get("/config", response_class=HTMLResponse)
async def config(request: Request):
    return saleor_app.templates.TemplateResponse("config.html", {
        "request": request
    })


# API endpoint for config update
@saleor_app.post("/api/config/update", response_class=HTMLResponse)
async def update_config(
    request: Request,
    app_name: str = Form(...),
    api_url: str = Form(""),
    secret_key: str = Form(""),
    webhooks: List[str] = Form([])
):
    try:
        # In a real app, you would save these settings to a database or config file
        logger.info(f"Updating config: app_name={app_name}, webhooks={webhooks}")

        # For demo purposes, just log the values
        logger.info(f"API URL: {api_url}")
        logger.info(f"Webhooks: {webhooks}")

        # Return success response
        return saleor_app.templates.TemplateResponse(
            "partials/config_updated.html", 
            {"request": request, "success": True}
        )
    except Exception as e:
        logger.exception("Error updating config: %s", e)
        return saleor_app.templates.TemplateResponse(
            "partials/config_updated.html", 
            {"request": request, "success": False, "error": str(e)}
        )

# API endpoints for product operations
@saleor_app.get("/api/products/search", response_class=HTMLResponse)
async def search_products(request: Request, query: str = ""):
    # Get the first installation (in a real app, you'd get the installation for the specific domain)
    installations = list(saleor_app.installations.values())
    if not installations:
        return saleor_app.templates.TemplateResponse(
            "partials/product_search_results.html", 
            {"request": request, "products": [], "error": "No Saleor installation found"}
        )

    installation = installations[0]
    client = saleor_app.get_graphql_client(installation.domain)

    try:
        # Execute the search query
        result = await client.execute_async(
            PRODUCT_SEARCH_QUERY, 
            variables={"search": query, "first": 20}
        )

        # Transform the result to a more usable format
        products = []
        for edge in result.get("products", {}).get("edges", []):
            node = edge.get("node", {})
            pricing = node.get("pricing", {}).get("priceRange", {}).get("start", {}).get("gross", {})

            products.append({
                "id": node.get("id"),
                "name": node.get("name"),
                "description": node.get("description"),
                "is_published": node.get("isPublished"),
                "price": pricing.get("amount"),
                "currency": pricing.get("currency")
            })

        return saleor_app.templates.TemplateResponse(
            "partials/product_search_results.html", 
            {"request": request, "products": products, "last_query": query}
        )
    except Exception as e:
        logger.exception("Error searching products: %s", e)
        return saleor_app.templates.TemplateResponse(
            "partials/product_search_results.html", 
            {"request": request, "products": [], "error": str(e)}
        )


@saleor_app.get("/api/products/{product_id}", response_class=HTMLResponse)
async def get_product(request: Request, product_id: str):
    # Get the first installation (in a real app, you'd get the installation for the specific domain)
    installations = list(saleor_app.installations.values())
    if not installations:
        return {"error": "No Saleor installation found"}

    installation = installations[0]
    client = saleor_app.get_graphql_client(installation.domain)

    try:
        # Execute the product details query
        result = await client.execute_async(
            PRODUCT_DETAILS_QUERY, 
            variables={"id": product_id}
        )

        product_data = result.get("product", {})
        pricing = product_data.get("pricing", {}).get("priceRange", {}).get("start", {}).get("gross", {})

        product = {
            "id": product_data.get("id"),
            "name": product_data.get("name"),
            "description": product_data.get("description"),
            "is_published": product_data.get("isPublished"),
            "price": pricing.get("amount"),
            "currency": pricing.get("currency")
        }

        return saleor_app.templates.TemplateResponse(
            "partials/product_details.html", 
            {"request": request, "product": product}
        )
    except Exception as e:
        logger.exception("Error getting product: %s", e)
        return {"error": str(e)}


@saleor_app.post("/api/products/create", response_class=HTMLResponse)
async def create_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    currency: str = Form(...)
):
    # Get the first installation (in a real app, you'd get the installation for the specific domain)
    installations = list(saleor_app.installations.values())
    if not installations:
        return saleor_app.templates.TemplateResponse(
            "partials/product_created.html", 
            {"request": request, "success": False, "error": "No Saleor installation found"}
        )

    installation = installations[0]
    client = saleor_app.get_graphql_client(installation.domain)

    try:
        # Prepare input for product creation
        input_data = {
            "name": name,
            "description": description,
            "productType": "UHJvZHVjdFR5cGU6MQ==",  # This should be a valid product type ID from your Saleor instance
            "basePrice": price,
            "isPublished": True
        }

        # Execute the create product mutation
        result = await client.execute_async(
            CREATE_PRODUCT_MUTATION, 
            variables={"input": input_data}
        )

        product_create = result.get("productCreate", {})
        errors = product_create.get("errors", [])

        if errors:
            error_message = "; ".join([f"{e.get('field')}: {e.get('message')}" for e in errors])
            return saleor_app.templates.TemplateResponse(
                "partials/product_created.html", 
                {"request": request, "success": False, "error": error_message}
            )

        product = product_create.get("product", {})

        return saleor_app.templates.TemplateResponse(
            "partials/product_created.html", 
            {
                "request": request, 
                "success": True, 
                "product": {
                    "id": product.get("id"),
                    "name": product.get("name")
                }
            }
        )
    except Exception as e:
        logger.exception("Error creating product: %s", e)
        return saleor_app.templates.TemplateResponse(
            "partials/product_created.html", 
            {"request": request, "success": False, "error": str(e)}
        )


# Handle a webhook example
@saleor_app.webhook(WebhookEventType.ORDER_CREATED)
async def handle_order_created(payload, installation):
    logger.info("Get order created webhook: %s", payload)

    # Use GraphQL client to interact with Saleor API
    saleor_app.get_graphql_client(installation.domain)
    # ... process the order

    return {"status": "success"}


# Handle product webhooks
@saleor_app.webhook(WebhookEventType.PRODUCT_CREATED)
async def handle_product_created(payload, installation):
    logger.info("Product created webhook: %s", payload)
    return {"status": "success"}


@saleor_app.webhook(WebhookEventType.PRODUCT_UPDATED)
async def handle_product_updated(payload, installation):
    logger.info("Product updated webhook: %s", payload)
    return {"status": "success"}
