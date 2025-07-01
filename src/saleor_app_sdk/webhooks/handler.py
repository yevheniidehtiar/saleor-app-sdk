"""
Webhook handler for Saleor App SDK
"""

import asyncio
import hashlib
import hmac
import json
import logging
from collections.abc import Callable

from fastapi import HTTPException, Request

from .events import WebhookEventType

logger = logging.getLogger(__name__)


class WebhookHandler:
    """Handle incoming webhooks from Saleor"""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self._handlers: dict[WebhookEventType, Callable] = {}

    def register_handler(self, event_type: WebhookEventType, handler: Callable):
        """Register a handler for specific webhook event"""
        self._handlers[event_type] = handler

    def on(self, event_type: WebhookEventType):
        """Decorator to register webhook handlers"""

        def decorator(func: Callable):
            self.register_handler(event_type, func)
            return func

        return decorator

    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """Verify webhook signature"""
        expected_signature = hmac.new(
            self.secret_key.encode(), payload, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected_signature)

    async def process_webhook(self, request: Request) -> dict:
        """Process incoming webhook request"""
        body = await request.body()
        signature = request.headers.get("saleor-signature", "")

        if not self.verify_signature(body, signature):
            raise HTTPException(status_code=401, detail="Invalid signature")

        try:
            data = json.loads(body)
            event_type = WebhookEventType(request.headers.get("saleor-event", ""))

            if event_type in self._handlers:
                handler = self._handlers[event_type]
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
        except Exception as e:
            logger.exception("Webhook processing failed")
            raise HTTPException(status_code=400, detail=str(e)) from e
        else:
            # Return success response in the else block
            return {"received": True}
