import hashlib
import hmac
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from saleor_app_sdk.webhooks.events import WebhookEventType
from saleor_app_sdk.webhooks.handler import WebhookHandler


class TestWebhookHandler:
    def test_init(self, secret_key):
        """Test initialization of WebhookHandler"""
        handler = WebhookHandler(secret_key=secret_key)

        assert handler.secret_key == secret_key
        assert handler._handlers == {}

    def test_register_handler(self, webhook_handler):
        """Test registering a handler for a webhook event"""
        event_type = WebhookEventType.ORDER_CREATED
        handler_func = MagicMock()

        webhook_handler.register_handler(event_type, handler_func)

        assert webhook_handler._handlers[event_type] == handler_func

    def test_on_decorator(self, webhook_handler):
        """Test the 'on' decorator for registering handlers"""
        event_type = WebhookEventType.ORDER_CREATED

        @webhook_handler.on(event_type)
        def handler_func(data):
            return data

        assert webhook_handler._handlers[event_type] == handler_func

    def test_verify_signature_valid(
        self, webhook_handler, webhook_payload_bytes, webhook_signature
    ):
        """Test verifying a valid webhook signature"""
        is_valid = webhook_handler.verify_signature(
            webhook_payload_bytes, webhook_signature
        )

        assert is_valid is True

    def test_verify_signature_invalid(self, webhook_handler, webhook_payload_bytes):
        """Test verifying an invalid webhook signature"""
        invalid_signature = "invalid-signature"

        is_valid = webhook_handler.verify_signature(
            webhook_payload_bytes, invalid_signature
        )

        assert is_valid is False

    @pytest.mark.asyncio
    async def test_process_webhook_invalid_signature(self, webhook_handler):
        """Test processing a webhook with an invalid signature"""
        # Create a mock request with invalid signature
        mock_request = MagicMock()
        mock_request.body = AsyncMock(return_value=b'{"test": "data"}')
        mock_request.headers = {"saleor-signature": "invalid-signature"}

        with pytest.raises(HTTPException) as excinfo:
            await webhook_handler.process_webhook(mock_request)

        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Invalid signature"

    @pytest.mark.asyncio
    async def test_process_webhook_no_handler(
        self, webhook_handler, webhook_payload_bytes, webhook_signature
    ):
        """Test processing a webhook with no registered handler"""
        # Create a mock request with valid signature but no handler
        mock_request = MagicMock()
        mock_request.body = AsyncMock(return_value=webhook_payload_bytes)
        mock_request.headers = {
            "saleor-signature": webhook_signature,
            "saleor-event": WebhookEventType.ORDER_CREATED.value,
        }

        # No handler registered for ORDER_CREATED

        response = await webhook_handler.process_webhook(mock_request)

        # Should return success even if no handler is registered
        assert response == {"received": True}

    @pytest.mark.asyncio
    async def test_process_webhook_sync_handler(
        self, webhook_handler, webhook_payload_bytes, webhook_signature, webhook_payload
    ):
        """Test processing a webhook with a synchronous handler"""
        event_type = WebhookEventType.ORDER_CREATED

        # Register a synchronous handler
        handler_mock = MagicMock()
        webhook_handler.register_handler(event_type, handler_mock)

        # Create a mock request
        mock_request = MagicMock()
        mock_request.body = AsyncMock(return_value=webhook_payload_bytes)
        mock_request.headers = {
            "saleor-signature": webhook_signature,
            "saleor-event": event_type.value,
        }

        response = await webhook_handler.process_webhook(mock_request)

        # Verify handler was called with the payload
        handler_mock.assert_called_once_with(webhook_payload)
        assert response == {"received": True}

    @pytest.mark.asyncio
    async def test_process_webhook_async_handler(
        self, webhook_handler, webhook_payload_bytes, webhook_signature, webhook_payload
    ):
        """Test processing a webhook with an asynchronous handler"""
        event_type = WebhookEventType.ORDER_CREATED

        # Register an asynchronous handler
        handler_mock = AsyncMock()
        webhook_handler.register_handler(event_type, handler_mock)

        # Create a mock request
        mock_request = MagicMock()
        mock_request.body = AsyncMock(return_value=webhook_payload_bytes)
        mock_request.headers = {
            "saleor-signature": webhook_signature,
            "saleor-event": event_type.value,
        }

        response = await webhook_handler.process_webhook(mock_request)

        # Verify handler was called with the payload
        handler_mock.assert_called_once_with(webhook_payload)
        assert response == {"received": True}

    @pytest.mark.asyncio
    async def test_process_webhook_invalid_json(self, webhook_handler, secret_key):
        """Test processing a webhook with invalid JSON"""
        # Create invalid JSON payload
        invalid_payload = b'{"invalid": json'

        # Calculate signature for the invalid payload
        signature = hmac.new(
            secret_key.encode(), invalid_payload, hashlib.sha256
        ).hexdigest()

        # Create a mock request
        mock_request = MagicMock()
        mock_request.body = AsyncMock(return_value=invalid_payload)
        mock_request.headers = {
            "saleor-signature": signature,
            "saleor-event": WebhookEventType.ORDER_CREATED.value,
        }

        with pytest.raises(HTTPException) as excinfo:
            await webhook_handler.process_webhook(mock_request)

        assert excinfo.value.status_code == 400
        # The exact error message may vary depending on the JSON parser
        assert "Expecting" in excinfo.value.detail or "Invalid" in excinfo.value.detail

    @pytest.mark.asyncio
    async def test_process_webhook_invalid_event_type(
        self, webhook_handler, webhook_payload_bytes, secret_key
    ):
        """Test processing a webhook with an invalid event type"""
        # Calculate signature for the payload
        signature = hmac.new(
            secret_key.encode(), webhook_payload_bytes, hashlib.sha256
        ).hexdigest()

        # Create a mock request with invalid event type
        mock_request = MagicMock()
        mock_request.body = AsyncMock(return_value=webhook_payload_bytes)
        mock_request.headers = {
            "saleor-signature": signature,
            "saleor-event": "INVALID_EVENT_TYPE",
        }

        with pytest.raises(HTTPException) as excinfo:
            await webhook_handler.process_webhook(mock_request)

        assert excinfo.value.status_code == 400
        assert "is not a valid WebhookEventType" in excinfo.value.detail

    @pytest.mark.asyncio
    async def test_process_webhook_handler_exception(
        self, webhook_handler, webhook_payload_bytes, webhook_signature, webhook_payload
    ):
        """Test processing a webhook where the handler raises an exception"""
        event_type = WebhookEventType.ORDER_CREATED

        # Register a handler that raises an exception
        def handler_with_exception(data):
            error_msg = "Handler error"
            raise ValueError(error_msg)

        webhook_handler.register_handler(event_type, handler_with_exception)

        # Create a mock request
        mock_request = MagicMock()
        mock_request.body = AsyncMock(return_value=webhook_payload_bytes)
        mock_request.headers = {
            "saleor-signature": webhook_signature,
            "saleor-event": event_type.value,
        }

        with pytest.raises(HTTPException) as excinfo:
            await webhook_handler.process_webhook(mock_request)

        assert excinfo.value.status_code == 400
        assert "Handler error" in excinfo.value.detail
