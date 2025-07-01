"""
Builder pattern for creating Saleor apps
"""

from ..models.app_manifest import AppManifest
from ..models.webhooks import WebhookDefinition
from ..permissions import SaleorPermission
from ..webhooks.events import WebhookEventType
from .core import SaleorApp


class SaleorAppBuilder:
    """Builder pattern for creating Saleor apps"""

    def __init__(self, app_id: str, name: str):
        self._manifest = AppManifest(
            id=app_id,
            name=name,
            version="1.0.0",
            about="",
            permissions=[],
            app_url="",
            webhooks=[],
        )
        self._secret_key = None
        self._base_url = None

    def version(self, version: str):
        self._manifest.version = version
        return self

    def about(self, description: str):
        self._manifest.about = description
        return self

    def permissions(self, *permissions: SaleorPermission):
        self._manifest.permissions = list(permissions)
        return self

    def urls(self, app_url: str, config_url: str | None = None, **kwargs):
        self._manifest.app_url = app_url
        self._manifest.configuration_url = config_url
        self._manifest.data_privacy_url = kwargs.get("privacy_url")
        self._manifest.homepage_url = kwargs.get("homepage_url")
        self._manifest.support_url = kwargs.get("support_url")
        return self

    def webhook(
        self, name: str, events: list[WebhookEventType], query: str, target_url: str
    ):
        if not self._manifest.webhooks:
            self._manifest.webhooks = []
        self._manifest.webhooks.append(
            WebhookDefinition(name, events, query, target_url)
        )
        return self

    def secret_key(self, key: str):
        self._secret_key = key
        return self

    def base_url(self, url: str):
        self._base_url = url
        return self

    def build(self) -> SaleorApp:
        if not self._secret_key:
            error_msg = "Secret key is required"
            raise ValueError(error_msg)
        return SaleorApp(self._manifest, self._secret_key, self._base_url)
