# Saleor App SDK for Python

<a href="https://github.com/yevhenii./saleor-app-sdk-py/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/saleor/saleor-app-sdk-py/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://codecov.io/gh/saleor/saleor-app-sdk-py" target="_blank">
    <img src="https://codecov.io/gh/saleor/saleor-app-sdk-py/branch/master/graph/badge.svg" alt="Coverage">
</a>

A Python SDK for building Saleor apps with FastAPI and HTMX.

## Overview

Saleor App SDK provides a streamlined way to build apps for the Saleor e-commerce platform using Python. It offers a set of tools and utilities to handle common tasks such as app installation, webhook processing, and GraphQL API communication.

## Installation

```bash
pip install saleor-app-sdk
```

## Quick Start

### Creating a new Saleor app

The SDK includes a CLI tool to quickly scaffold a new Saleor app:

```bash
# Create a basic app
saleor-app create my-saleor-app

# Create an app with webhook handling
saleor-app create my-webhook-app --template webhook

# Create an app with UI components
saleor-app create my-ui-app --template ui
```

### Building a Saleor app manually

```python
from saleor_app_sdk import (
    SaleorApp, SaleorAppBuilder, SaleorPermission,
    WebhookEventType
)

# Create your Saleor app
app = (SaleorAppBuilder("my-app", "My Saleor App")
       .version("1.0.0")
       .about("A custom Saleor app built with saleor-app-sdk")
       .permissions(SaleorPermission.MANAGE_ORDERS)
       .urls(
           app_url="https://example.com/app",
           config_url="https://example.com/config"
       )
       .secret_key("your-secret-key")  # Change this in production!
       .base_url("https://example.com")
       .build())

# Access the FastAPI app
fastapi_app = app.fastapi_app

@app.get("/")
async def index():
    return {"message": "Welcome to my Saleor app!"}

# Handle a webhook
@app.webhook(WebhookEventType.ORDER_CREATED)
async def handle_order_created(payload, installation):
    order_id = payload["order"]["id"]
    print(f"New order created: {order_id}")

    # Use GraphQL client to interact with Saleor API
    client = app.get_graphql_client(installation.domain)
    # ... process the order
```

## Key Components

### SaleorAppBuilder

A builder pattern for creating and configuring Saleor apps with a fluent API.

### SaleorApp

The core class that handles app registration, webhook processing, and provides access to the FastAPI application.

### SaleorGraphQLClient

A client for making GraphQL requests to the Saleor API.

### WebhookHandler

Processes incoming webhooks from Saleor and routes them to the appropriate handlers.

### AppInstallation

Represents an installation of your app in a Saleor instance, containing authentication tokens and domain information.

## Development

### Requirements

- Python 3.11+
- FastAPI
- Uvicorn
- GQL for GraphQL

### Setting up a development environment

```bash
# Clone the repository
git clone https://github.com/saleor/saleor-app-sdk-python.git
cd saleor-app-sdk-python

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT
