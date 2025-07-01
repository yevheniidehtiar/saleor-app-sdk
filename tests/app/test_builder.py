import pytest
from unittest.mock import patch

from saleor_app_sdk.app.builder import SaleorAppBuilder
from saleor_app_sdk.app.core import SaleorApp
from saleor_app_sdk.permissions import SaleorPermission
from saleor_app_sdk.webhooks.events import WebhookEventType


class TestSaleorAppBuilder:
    def test_init(self, app_id, app_name):
        """Test initialization of SaleorAppBuilder"""
        builder = SaleorAppBuilder(app_id=app_id, name=app_name)
        
        assert builder._manifest.id == app_id
        assert builder._manifest.name == app_name
        assert builder._manifest.version == "1.0.0"
        assert builder._manifest.about == ""
        assert builder._manifest.permissions == []
        assert builder._manifest.app_url == ""
        assert builder._manifest.webhooks == []
        assert builder._secret_key is None
        assert builder._base_url is None

    def test_version(self, app_builder, app_version):
        """Test setting app version"""
        builder = app_builder.version(app_version)
        
        assert builder._manifest.version == app_version
        assert builder is app_builder  # Test method chaining

    def test_about(self, app_builder, app_about):
        """Test setting app description"""
        builder = app_builder.about(app_about)
        
        assert builder._manifest.about == app_about
        assert builder is app_builder  # Test method chaining

    def test_permissions(self, app_builder):
        """Test setting app permissions"""
        permissions = [SaleorPermission.MANAGE_ORDERS, SaleorPermission.MANAGE_PRODUCTS]
        builder = app_builder.permissions(*permissions)
        
        assert builder._manifest.permissions == permissions
        assert builder is app_builder  # Test method chaining

    def test_urls(self, app_builder, app_url, config_url):
        """Test setting app URLs"""
        privacy_url = "https://example.com/privacy"
        homepage_url = "https://example.com"
        support_url = "https://example.com/support"
        
        builder = app_builder.urls(
            app_url=app_url,
            config_url=config_url,
            privacy_url=privacy_url,
            homepage_url=homepage_url,
            support_url=support_url
        )
        
        assert builder._manifest.app_url == app_url
        assert builder._manifest.configuration_url == config_url
        assert builder._manifest.data_privacy_url == privacy_url
        assert builder._manifest.homepage_url == homepage_url
        assert builder._manifest.support_url == support_url
        assert builder is app_builder  # Test method chaining

    def test_webhook(self, app_builder, webhook_name, webhook_events, webhook_query, webhook_target_url):
        """Test adding a webhook"""
        builder = app_builder.webhook(
            name=webhook_name,
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url
        )
        
        assert len(builder._manifest.webhooks) == 1
        webhook = builder._manifest.webhooks[0]
        assert webhook.name == webhook_name
        assert webhook.events == webhook_events
        assert webhook.query == webhook_query
        assert webhook.target_url == webhook_target_url
        assert webhook.is_active is True
        assert builder is app_builder  # Test method chaining

    def test_multiple_webhooks(self, app_builder, webhook_name, webhook_events, webhook_query, webhook_target_url):
        """Test adding multiple webhooks"""
        # Add first webhook
        app_builder.webhook(
            name=webhook_name,
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url
        )
        
        # Add second webhook
        second_webhook_name = "Second Webhook"
        second_webhook_events = [WebhookEventType.PRODUCT_CREATED]
        second_webhook_query = "query { product { id } }"
        second_webhook_target_url = "https://example.com/webhooks/product"
        
        app_builder.webhook(
            name=second_webhook_name,
            events=second_webhook_events,
            query=second_webhook_query,
            target_url=second_webhook_target_url
        )
        
        assert len(app_builder._manifest.webhooks) == 2
        
        # Check first webhook
        webhook1 = app_builder._manifest.webhooks[0]
        assert webhook1.name == webhook_name
        assert webhook1.events == webhook_events
        
        # Check second webhook
        webhook2 = app_builder._manifest.webhooks[1]
        assert webhook2.name == second_webhook_name
        assert webhook2.events == second_webhook_events

    def test_secret_key(self, app_builder, secret_key):
        """Test setting secret key"""
        builder = app_builder.secret_key(secret_key)
        
        assert builder._secret_key == secret_key
        assert builder is app_builder  # Test method chaining

    def test_base_url(self, app_builder, base_url):
        """Test setting base URL"""
        builder = app_builder.base_url(base_url)
        
        assert builder._base_url == base_url
        assert builder is app_builder  # Test method chaining

    def test_build_without_secret_key(self, app_builder):
        """Test building app without secret key raises ValueError"""
        with pytest.raises(ValueError, match="Secret key is required"):
            app_builder.build()

    def test_build_success(self, app_builder, secret_key, base_url):
        """Test successful app building"""
        app_builder.secret_key(secret_key).base_url(base_url)
        app = app_builder.build()
        
        assert isinstance(app, SaleorApp)
        assert app.manifest == app_builder._manifest
        assert app.secret_key == secret_key
        assert app.base_url == base_url