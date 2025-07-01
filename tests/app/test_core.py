import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import Request
from fastapi.testclient import TestClient

from saleor_app_sdk.app.core import SaleorApp
from saleor_app_sdk.graphql.client import SaleorGraphQLClient
from saleor_app_sdk.models.installation import AppInstallation
from saleor_app_sdk.webhooks.events import WebhookEventType


class TestSaleorApp:
    def test_init(self, app_manifest, secret_key, base_url):
        """Test initialization of SaleorApp"""
        app = SaleorApp(manifest=app_manifest, secret_key=secret_key, base_url=base_url)

        assert app.manifest == app_manifest
        assert app.secret_key == secret_key
        assert app.base_url == base_url
        assert app.fastapi_app is not None
        assert app.templates is not None
        assert app.webhook_handler is not None
        assert app.installations == {}

    def test_get_manifest_route(self, test_client, saleor_app, app_manifest, base_url):
        """Test GET /api/manifest route"""
        response = test_client.get("/api/manifest")

        assert response.status_code == 200
        data = response.json()

        assert data["id"] == app_manifest.id
        assert data["name"] == app_manifest.name
        assert data["version"] == app_manifest.version
        assert data["about"] == app_manifest.about
        assert data["permissions"] == [p.value for p in app_manifest.permissions]
        assert data["appUrl"] == app_manifest.app_url
        assert data["tokenTargetUrl"] == f"{base_url}/api/register"

    def test_register_installation_route(self, test_client, domain, auth_token):
        """Test POST /api/register route"""
        data = {
            "auth_token": auth_token,
            "domain": domain,
        }

        response = test_client.post("/api/register", json=data)

        assert response.status_code == 200
        assert response.json() == {"success": True}

    def test_register_installation_with_custom_handler(self, app_manifest, secret_key, base_url):
        """Test registration with custom on_install handler"""
        # Create a custom app class with an on_install handler
        class CustomApp(SaleorApp):
            async def on_install(self, installation: AppInstallation):
                self.custom_handler_called = True
                self.installed_domain = installation.domain

        app = CustomApp(manifest=app_manifest, secret_key=secret_key, base_url=base_url)
        app.custom_handler_called = False

        # Create a test client for the custom app
        client = TestClient(app.fastapi_app)

        # Send a registration request
        data = {
            "auth_token": "custom-token",
            "domain": "custom.domain.com",
        }

        response = client.post("/api/register", json=data)

        assert response.status_code == 200
        assert response.json() == {"success": True}
        assert app.custom_handler_called is True
        assert app.installed_domain == "custom.domain.com"

    def test_webhook_route(self, test_client):
        """Test POST /api/webhooks/{event_type} route"""
        # This test will be expanded in the webhook handler tests
        # Here we just check that the route exists and returns 401 for invalid signature
        response = test_client.post("/api/webhooks/ORDER_CREATED", json={})

        # When sending a request without the required headers, we get a validation error
        assert response.status_code == 422
        assert "detail" in response.json()

    def test_serialize_manifest_basic(self, saleor_app, app_manifest, base_url):
        """Test serialization of basic app manifest"""
        manifest_dict = saleor_app._serialize_manifest()

        assert manifest_dict["id"] == app_manifest.id
        assert manifest_dict["name"] == app_manifest.name
        assert manifest_dict["version"] == app_manifest.version
        assert manifest_dict["about"] == app_manifest.about
        assert manifest_dict["permissions"] == [p.value for p in app_manifest.permissions]
        assert manifest_dict["appUrl"] == app_manifest.app_url
        assert manifest_dict["tokenTargetUrl"] == f"{base_url}/api/register"
        assert manifest_dict["webhooks"] == []

    def test_serialize_manifest_with_urls(self, app_manifest, secret_key, base_url):
        """Test serialization of app manifest with additional URLs"""
        app_manifest.configuration_url = "https://example.com/config"
        app_manifest.data_privacy_url = "https://example.com/privacy"
        app_manifest.homepage_url = "https://example.com"
        app_manifest.support_url = "https://example.com/support"

        app = SaleorApp(manifest=app_manifest, secret_key=secret_key, base_url=base_url)
        manifest_dict = app._serialize_manifest()

        assert manifest_dict["configurationUrl"] == app_manifest.configuration_url
        assert manifest_dict["dataPrivacyUrl"] == app_manifest.data_privacy_url
        assert manifest_dict["homepageUrl"] == app_manifest.homepage_url
        assert manifest_dict["supportUrl"] == app_manifest.support_url

    def test_serialize_manifest_with_webhooks(self, app_manifest, secret_key, base_url, webhook_definition):
        """Test serialization of app manifest with webhooks"""
        app_manifest.webhooks = [webhook_definition]

        app = SaleorApp(manifest=app_manifest, secret_key=secret_key, base_url=base_url)
        manifest_dict = app._serialize_manifest()

        assert len(manifest_dict["webhooks"]) == 1
        webhook = manifest_dict["webhooks"][0]
        assert webhook["name"] == webhook_definition.name
        assert webhook["asyncEvents"] == [e.value for e in webhook_definition.events]
        assert webhook["query"] == webhook_definition.query
        assert webhook["targetUrl"] == webhook_definition.target_url
        assert webhook["isActive"] == webhook_definition.is_active

    def test_get_installation(self, saleor_app, app_installation, domain):
        """Test getting app installation by domain"""
        # Add installation to the app
        saleor_app.installations[domain] = app_installation

        # Get the installation
        installation = saleor_app.get_installation(domain)

        assert installation is app_installation

        # Test getting non-existent installation
        assert saleor_app.get_installation("non-existent.domain") is None

    def test_get_graphql_client(self, saleor_app, app_installation, domain):
        """Test getting GraphQL client for installation"""
        # Add installation to the app
        saleor_app.installations[domain] = app_installation

        # Get the GraphQL client
        client = saleor_app.get_graphql_client(domain)

        assert isinstance(client, SaleorGraphQLClient)
        assert client.api_url == app_installation.saleor_api_url
        assert client.auth_token == app_installation.auth_token

        # Test getting client for non-existent installation
        assert saleor_app.get_graphql_client("non-existent.domain") is None

    def test_route_decorator(self, saleor_app):
        """Test route decorator"""
        with patch.object(saleor_app.fastapi_app, "route") as mock_route:
            @saleor_app.route("/test", methods=["GET"])
            def test_route():
                return {"message": "test"}

            mock_route.assert_called_once_with("/test", methods=["GET"])

    def test_get_decorator(self, saleor_app):
        """Test get decorator"""
        with patch.object(saleor_app.fastapi_app, "get") as mock_get:
            @saleor_app.get("/test")
            def test_route():
                return {"message": "test"}

            mock_get.assert_called_once_with("/test")

    def test_post_decorator(self, saleor_app):
        """Test post decorator"""
        with patch.object(saleor_app.fastapi_app, "post") as mock_post:
            @saleor_app.post("/test")
            def test_route():
                return {"message": "test"}

            mock_post.assert_called_once_with("/test")

    def test_webhook_decorator(self, saleor_app):
        """Test webhook decorator"""
        with patch.object(saleor_app.webhook_handler, "on") as mock_on:
            @saleor_app.webhook(WebhookEventType.ORDER_CREATED)
            def test_webhook(data):
                return data

            mock_on.assert_called_once_with(WebhookEventType.ORDER_CREATED)

    def test_on_install_hook(self, saleor_app, app_installation):
        """Test on_install hook"""
        # The default implementation should do nothing
        # We just verify it can be called without errors
        import asyncio
        asyncio.run(saleor_app.on_install(app_installation))

    def test_on_uninstall_hook(self, saleor_app, app_installation):
        """Test on_uninstall hook"""
        # The default implementation should do nothing
        # We just verify it can be called without errors
        import asyncio
        asyncio.run(saleor_app.on_uninstall(app_installation))
