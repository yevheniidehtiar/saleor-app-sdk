from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from saleor_app_sdk.app.builder import SaleorAppBuilder
from saleor_app_sdk.app.core import SaleorApp
from saleor_app_sdk.models.app_manifest import AppManifest
from saleor_app_sdk.models.installation import AppInstallation
from saleor_app_sdk.models.webhooks import WebhookDefinition
from saleor_app_sdk.permissions import SaleorPermission
from saleor_app_sdk.webhooks.events import WebhookEventType
from saleor_app_sdk.webhooks.handler import WebhookHandler


@pytest.fixture
def app_id():
    return "test-app-id"


@pytest.fixture
def app_name():
    return "Test App"


@pytest.fixture
def app_version():
    return "1.0.0"


@pytest.fixture
def app_about():
    return "Test app description"


@pytest.fixture
def app_url():
    return "https://example.com/app"


@pytest.fixture
def config_url():
    return "https://example.com/config"


@pytest.fixture
def secret_key():
    return "test-secret-key"


@pytest.fixture
def base_url():
    return "https://example.com"


@pytest.fixture
def webhook_name():
    return "Test Webhook"


@pytest.fixture
def webhook_events():
    return [WebhookEventType.ORDER_CREATED, WebhookEventType.ORDER_UPDATED]


@pytest.fixture
def webhook_query():
    return """
    query OrderInfo($id: ID!) {
        order(id: $id) {
            id
            number
            status
        }
    }
    """


@pytest.fixture
def webhook_target_url():
    return "https://example.com/webhooks/order"


@pytest.fixture
def webhook_definition(webhook_name, webhook_events, webhook_query, webhook_target_url):
    return WebhookDefinition(
        name=webhook_name,
        events=webhook_events,
        query=webhook_query,
        target_url=webhook_target_url,
    )


@pytest.fixture
def app_manifest(app_id, app_name, app_version, app_about, app_url):
    return AppManifest(
        id=app_id,
        name=app_name,
        version=app_version,
        about=app_about,
        permissions=[SaleorPermission.MANAGE_ORDERS, SaleorPermission.MANAGE_PRODUCTS],
        app_url=app_url,
    )


@pytest.fixture
def app_builder(app_id, app_name):
    return SaleorAppBuilder(app_id=app_id, name=app_name)


@pytest.fixture
def saleor_app(app_manifest, secret_key, base_url):
    return SaleorApp(
        manifest=app_manifest,
        secret_key=secret_key,
        base_url=base_url,
    )


@pytest.fixture
def test_client(saleor_app):
    return TestClient(saleor_app.fastapi_app)


@pytest.fixture
def domain():
    return "test.saleor.io"


@pytest.fixture
def auth_token():
    return "test-auth-token"


@pytest.fixture
def saleor_api_url(domain):
    return f"https://{domain}/graphql/"


@pytest.fixture
def app_installation(domain, auth_token, saleor_api_url):
    return AppInstallation(
        auth_token=auth_token,
        domain=domain,
        saleor_api_url=saleor_api_url,
        installed_at=datetime.now(UTC),
    )


@pytest.fixture
def mock_gql_client():
    with patch("saleor_app_sdk.graphql.client.Client") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_instance.execute.return_value = {"data": {"test": "value"}}
        yield mock_instance


@pytest.fixture
def mock_httpx_transport():
    with patch("saleor_app_sdk.graphql.client.HTTPXTransport") as mock_transport:
        yield mock_transport


@pytest.fixture
def webhook_handler(secret_key):
    return WebhookHandler(secret_key=secret_key)


@pytest.fixture
def webhook_payload():
    return {
        "order": {
            "id": "T3JkZXI6MQ==",
            "number": "1",
            "status": "UNFULFILLED",
        }
    }


@pytest.fixture
def webhook_payload_bytes(webhook_payload):
    import json

    return json.dumps(webhook_payload).encode()


@pytest.fixture
def webhook_signature(webhook_payload_bytes, secret_key):
    import hashlib
    import hmac

    return hmac.new(
        secret_key.encode(), webhook_payload_bytes, hashlib.sha256
    ).hexdigest()
