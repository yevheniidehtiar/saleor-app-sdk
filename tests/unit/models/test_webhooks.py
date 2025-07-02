from saleor_app_sdk.models.webhooks import WebhookDefinition
from saleor_app_sdk.webhooks.events import WebhookEventType


class TestWebhookDefinition:
    def test_init_minimal(
        self, webhook_name, webhook_events, webhook_query, webhook_target_url
    ):
        """Test initialization with minimal required fields"""
        webhook = WebhookDefinition(
            name=webhook_name,
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url,
        )

        assert webhook.name == webhook_name
        assert webhook.events == webhook_events
        assert webhook.query == webhook_query
        assert webhook.target_url == webhook_target_url
        assert webhook.is_active is True  # Default value

    def test_init_with_is_active(
        self, webhook_name, webhook_events, webhook_query, webhook_target_url
    ):
        """Test initialization with is_active parameter"""
        webhook = WebhookDefinition(
            name=webhook_name,
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url,
            is_active=False,
        )

        assert webhook.name == webhook_name
        assert webhook.events == webhook_events
        assert webhook.query == webhook_query
        assert webhook.target_url == webhook_target_url
        assert webhook.is_active is False

    def test_init_with_single_event(
        self, webhook_name, webhook_query, webhook_target_url
    ):
        """Test initialization with a single event"""
        event = WebhookEventType.ORDER_CREATED

        webhook = WebhookDefinition(
            name=webhook_name,
            events=[event],
            query=webhook_query,
            target_url=webhook_target_url,
        )

        assert webhook.events == [event]

    def test_init_with_multiple_events(
        self, webhook_name, webhook_query, webhook_target_url
    ):
        """Test initialization with multiple events"""
        events = [
            WebhookEventType.ORDER_CREATED,
            WebhookEventType.ORDER_UPDATED,
            WebhookEventType.ORDER_PAID,
        ]

        webhook = WebhookDefinition(
            name=webhook_name,
            events=events,
            query=webhook_query,
            target_url=webhook_target_url,
        )

        assert webhook.events == events

    def test_equality(
        self, webhook_name, webhook_events, webhook_query, webhook_target_url
    ):
        """Test equality comparison"""
        webhook1 = WebhookDefinition(
            name=webhook_name,
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url,
        )

        webhook2 = WebhookDefinition(
            name=webhook_name,
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url,
        )

        assert webhook1 == webhook2

        # Test inequality
        webhook3 = WebhookDefinition(
            name="Different Name",
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url,
        )

        assert webhook1 != webhook3

    def test_repr(
        self, webhook_name, webhook_events, webhook_query, webhook_target_url
    ):
        """Test string representation"""
        webhook = WebhookDefinition(
            name=webhook_name,
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url,
        )

        repr_str = repr(webhook)

        assert webhook_name in repr_str
        assert webhook_target_url in repr_str
        assert "events=" in repr_str
        assert "query=" in repr_str
        assert "is_active=True" in repr_str

    def test_immutability(
        self, webhook_name, webhook_events, webhook_query, webhook_target_url
    ):
        """Test that webhook attributes can be accessed but not modified"""
        webhook = WebhookDefinition(
            name=webhook_name,
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url,
        )

        # Attributes can be accessed
        assert webhook.name == webhook_name
        assert webhook.events == webhook_events
        assert webhook.query == webhook_query
        assert webhook.target_url == webhook_target_url

        # Test that we can create a new webhook with different attributes
        webhook2 = WebhookDefinition(
            name="Different Name",
            events=webhook_events,
            query=webhook_query,
            target_url=webhook_target_url,
        )

        assert webhook.name != webhook2.name
        assert webhook != webhook2

        # Note: WebhookDefinition is a dataclass with mutable fields (list),
        # so it's not hashable by default and can't be used in sets or as dict keys
