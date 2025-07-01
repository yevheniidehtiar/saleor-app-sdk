import pytest

from saleor_app_sdk.models.app_manifest import AppManifest
from saleor_app_sdk.permissions import SaleorPermission
from saleor_app_sdk.models.webhooks import WebhookDefinition
from saleor_app_sdk.webhooks.events import WebhookEventType


class TestAppManifest:
    def test_init_minimal(self, app_id, app_name, app_version, app_about, app_url):
        """Test initialization with minimal required fields"""
        manifest = AppManifest(
            id=app_id,
            name=app_name,
            version=app_version,
            about=app_about,
            permissions=[],
            app_url=app_url,
        )
        
        assert manifest.id == app_id
        assert manifest.name == app_name
        assert manifest.version == app_version
        assert manifest.about == app_about
        assert manifest.permissions == []
        assert manifest.app_url == app_url
        assert manifest.configuration_url is None
        assert manifest.token_target_url is None
        assert manifest.data_privacy_url is None
        assert manifest.homepage_url is None
        assert manifest.support_url is None
        assert manifest.webhooks is None
        assert manifest.extensions is None

    def test_init_with_permissions(self, app_id, app_name, app_version, app_about, app_url):
        """Test initialization with permissions"""
        permissions = [SaleorPermission.MANAGE_ORDERS, SaleorPermission.MANAGE_PRODUCTS]
        
        manifest = AppManifest(
            id=app_id,
            name=app_name,
            version=app_version,
            about=app_about,
            permissions=permissions,
            app_url=app_url,
        )
        
        assert manifest.permissions == permissions

    def test_init_with_urls(self, app_id, app_name, app_version, app_about, app_url):
        """Test initialization with additional URLs"""
        config_url = "https://example.com/config"
        token_url = "https://example.com/token"
        privacy_url = "https://example.com/privacy"
        homepage_url = "https://example.com"
        support_url = "https://example.com/support"
        
        manifest = AppManifest(
            id=app_id,
            name=app_name,
            version=app_version,
            about=app_about,
            permissions=[],
            app_url=app_url,
            configuration_url=config_url,
            token_target_url=token_url,
            data_privacy_url=privacy_url,
            homepage_url=homepage_url,
            support_url=support_url,
        )
        
        assert manifest.app_url == app_url
        assert manifest.configuration_url == config_url
        assert manifest.token_target_url == token_url
        assert manifest.data_privacy_url == privacy_url
        assert manifest.homepage_url == homepage_url
        assert manifest.support_url == support_url

    def test_init_with_webhooks(self, app_id, app_name, app_version, app_about, app_url, webhook_definition):
        """Test initialization with webhooks"""
        webhooks = [webhook_definition]
        
        manifest = AppManifest(
            id=app_id,
            name=app_name,
            version=app_version,
            about=app_about,
            permissions=[],
            app_url=app_url,
            webhooks=webhooks,
        )
        
        assert manifest.webhooks == webhooks

    def test_init_with_extensions(self, app_id, app_name, app_version, app_about, app_url):
        """Test initialization with extensions"""
        extensions = [
            {
                "label": "Test Extension",
                "mount": "NAVIGATION",
                "target": "APP_PAGE",
                "url": "https://example.com/extension",
                "permissions": ["MANAGE_ORDERS"],
            }
        ]
        
        manifest = AppManifest(
            id=app_id,
            name=app_name,
            version=app_version,
            about=app_about,
            permissions=[],
            app_url=app_url,
            extensions=extensions,
        )
        
        assert manifest.extensions == extensions

    def test_equality(self, app_id, app_name, app_version, app_about, app_url):
        """Test equality comparison"""
        manifest1 = AppManifest(
            id=app_id,
            name=app_name,
            version=app_version,
            about=app_about,
            permissions=[],
            app_url=app_url,
        )
        
        manifest2 = AppManifest(
            id=app_id,
            name=app_name,
            version=app_version,
            about=app_about,
            permissions=[],
            app_url=app_url,
        )
        
        assert manifest1 == manifest2
        
        # Test inequality
        manifest3 = AppManifest(
            id="different-id",
            name=app_name,
            version=app_version,
            about=app_about,
            permissions=[],
            app_url=app_url,
        )
        
        assert manifest1 != manifest3

    def test_repr(self, app_id, app_name, app_version, app_about, app_url):
        """Test string representation"""
        manifest = AppManifest(
            id=app_id,
            name=app_name,
            version=app_version,
            about=app_about,
            permissions=[],
            app_url=app_url,
        )
        
        repr_str = repr(manifest)
        
        assert app_id in repr_str
        assert app_name in repr_str
        assert app_version in repr_str
        assert app_about in repr_str
        assert app_url in repr_str