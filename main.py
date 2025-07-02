import logging
import os

from saleor_app_sdk import SaleorAppBuilder, SaleorPermission, WebhookEventType

# Create your Saleor app
saleor_app = (
    SaleorAppBuilder("saleor-app", "Saleor App")
    .version("0.1.0")
    .about("A Saleor app built with saleor-app-sdk")
    .permissions(SaleorPermission.MANAGE_ORDERS)
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


@saleor_app.get("/")
async def index():
    return {"message": "Welcome to Saleor App!"}


@saleor_app.get("/config")
async def config():
    return {"message": "App configuration page"}


# Handle a webhook example
@saleor_app.webhook(WebhookEventType.ORDER_CREATED)
async def handle_order_created(payload, installation):
    logger.info("Get order created webhook: %s", payload)

    # Use GraphQL client to interact with Saleor API
    saleor_app.get_graphql_client(installation.domain)
    # ... process the order

    return {"status": "success"}
