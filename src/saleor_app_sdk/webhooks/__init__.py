"""
Webhook-related functionality for Saleor App SDK
"""

from .events import WebhookEventType
from .handler import WebhookHandler

__all__ = ["WebhookEventType", "WebhookHandler"]
