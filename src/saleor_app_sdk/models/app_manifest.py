"""
App manifest model for Saleor App SDK
"""

from dataclasses import dataclass

from saleor_app_sdk.permissions import SaleorPermission

from .webhooks import WebhookDefinition


@dataclass
class AppManifest:
    id: str
    name: str
    version: str
    about: str
    permissions: list[SaleorPermission]
    app_url: str
    configuration_url: str | None = None
    token_target_url: str | None = None
    data_privacy_url: str | None = None
    homepage_url: str | None = None
    support_url: str | None = None
    webhooks: list[WebhookDefinition] = None
    extensions: list[dict] = None
