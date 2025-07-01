"""
Webhook-related models for Saleor App SDK
"""

from dataclasses import dataclass

from ..webhooks.events import WebhookEventType


@dataclass
class WebhookDefinition:
    name: str
    events: list[WebhookEventType]
    query: str
    target_url: str
    is_active: bool = True
