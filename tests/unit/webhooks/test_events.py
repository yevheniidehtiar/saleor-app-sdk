from enum import Enum

import pytest

from saleor_app_sdk.webhooks.events import WebhookEventType


class TestWebhookEventType:
    def test_is_enum(self):
        """Test that WebhookEventType is an Enum"""
        assert issubclass(WebhookEventType, Enum)
        assert issubclass(WebhookEventType, str)

    def test_order_events(self):
        """Test order-related event types"""
        assert WebhookEventType.ORDER_CREATED == "ORDER_CREATED"
        assert WebhookEventType.ORDER_UPDATED == "ORDER_UPDATED"
        assert WebhookEventType.ORDER_PAID == "ORDER_PAID"
        assert WebhookEventType.ORDER_FULLY_PAID == "ORDER_FULLY_PAID"
        assert WebhookEventType.ORDER_REFUNDED == "ORDER_REFUNDED"
        assert WebhookEventType.ORDER_CANCELLED == "ORDER_CANCELLED"
        assert WebhookEventType.ORDER_FULFILLED == "ORDER_FULFILLED"

    def test_product_events(self):
        """Test product-related event types"""
        assert WebhookEventType.PRODUCT_CREATED == "PRODUCT_CREATED"
        assert WebhookEventType.PRODUCT_UPDATED == "PRODUCT_UPDATED"
        assert WebhookEventType.PRODUCT_DELETED == "PRODUCT_DELETED"

    def test_customer_events(self):
        """Test customer-related event types"""
        assert WebhookEventType.CUSTOMER_CREATED == "CUSTOMER_CREATED"
        assert WebhookEventType.CUSTOMER_UPDATED == "CUSTOMER_UPDATED"

    def test_checkout_events(self):
        """Test checkout-related event types"""
        assert WebhookEventType.CHECKOUT_CREATED == "CHECKOUT_CREATED"
        assert WebhookEventType.CHECKOUT_UPDATED == "CHECKOUT_UPDATED"

    def test_enum_values(self):
        """Test that all enum values are strings and match their names"""
        for event_type in WebhookEventType:
            assert isinstance(event_type.value, str)
            assert event_type.value == event_type.name

    def test_enum_comparison(self):
        """Test enum comparison"""
        assert WebhookEventType.ORDER_CREATED == WebhookEventType.ORDER_CREATED
        assert WebhookEventType.ORDER_CREATED == "ORDER_CREATED"
        assert WebhookEventType.ORDER_CREATED != WebhookEventType.ORDER_UPDATED
        assert WebhookEventType.ORDER_CREATED != "ORDER_UPDATED"

    def test_enum_in_list(self):
        """Test enum in list"""
        events = [WebhookEventType.ORDER_CREATED, WebhookEventType.ORDER_UPDATED]

        assert WebhookEventType.ORDER_CREATED in events
        assert WebhookEventType.ORDER_PAID not in events
        # Check the string representation of the enum values
        assert all(f"WebhookEventType.{e.name}" == str(e) for e in events)

    def test_enum_as_dict_key(self):
        """Test enum as dictionary key"""
        event_handlers = {
            WebhookEventType.ORDER_CREATED: "handle_order_created",
            WebhookEventType.ORDER_UPDATED: "handle_order_updated",
        }

        assert event_handlers[WebhookEventType.ORDER_CREATED] == "handle_order_created"
        assert event_handlers[WebhookEventType.ORDER_UPDATED] == "handle_order_updated"
        assert WebhookEventType.ORDER_PAID not in event_handlers

    def test_enum_iteration(self):
        """Test enum iteration"""
        event_types = list(WebhookEventType)

        assert len(event_types) > 0
        assert WebhookEventType.ORDER_CREATED in event_types
        assert WebhookEventType.PRODUCT_CREATED in event_types
        assert WebhookEventType.CUSTOMER_CREATED in event_types
        assert WebhookEventType.CHECKOUT_CREATED in event_types

    def test_enum_from_string(self):
        """Test creating enum from string"""
        event_type = WebhookEventType("ORDER_CREATED")
        assert event_type == WebhookEventType.ORDER_CREATED

        with pytest.raises(ValueError):
            WebhookEventType("INVALID_EVENT")
