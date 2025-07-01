import pytest

from saleor_app_sdk.app.config import AppConfigMixin


class TestAppClass(AppConfigMixin):
    """Test class that uses AppConfigMixin"""
    def __init__(self):
        super().__init__()


class TestAppConfigMixin:
    def test_init(self):
        """Test initialization of AppConfigMixin"""
        app = TestAppClass()
        
        assert hasattr(app, "config_storage")
        assert app.config_storage == {}

    def test_get_config_empty(self):
        """Test getting config for domain with no config"""
        app = TestAppClass()
        domain = "test.saleor.io"
        
        # Get config for domain with no config
        config = app.get_config(domain)
        assert config == {}
        
        # Get config with default value
        default_config = {"key": "value"}
        config = app.get_config(domain, default_config)
        assert config == default_config

    def test_set_config(self):
        """Test setting config for domain"""
        app = TestAppClass()
        domain = "test.saleor.io"
        config = {"api_key": "12345", "webhook_secret": "secret"}
        
        # Set config for domain
        app.set_config(domain, config)
        
        # Verify config was set
        assert app.config_storage[domain] == config
        assert app.get_config(domain) == config

    def test_update_config_empty(self):
        """Test updating config for domain with no existing config"""
        app = TestAppClass()
        domain = "test.saleor.io"
        updates = {"api_key": "12345"}
        
        # Update config for domain with no existing config
        app.update_config(domain, updates)
        
        # Verify config was created with updates
        assert app.config_storage[domain] == updates
        assert app.get_config(domain) == updates

    def test_update_config_existing(self):
        """Test updating existing config for domain"""
        app = TestAppClass()
        domain = "test.saleor.io"
        
        # Set initial config
        initial_config = {"api_key": "12345", "webhook_secret": "secret"}
        app.set_config(domain, initial_config)
        
        # Update config
        updates = {"api_key": "67890", "new_key": "new_value"}
        app.update_config(domain, updates)
        
        # Verify config was updated correctly
        expected = {
            "api_key": "67890",  # Updated value
            "webhook_secret": "secret",  # Unchanged value
            "new_key": "new_value"  # New value
        }
        assert app.config_storage[domain] == expected
        assert app.get_config(domain) == expected

    def test_multiple_domains(self):
        """Test managing configs for multiple domains"""
        app = TestAppClass()
        
        # Set configs for different domains
        domain1 = "store1.saleor.io"
        config1 = {"api_key": "12345"}
        app.set_config(domain1, config1)
        
        domain2 = "store2.saleor.io"
        config2 = {"api_key": "67890"}
        app.set_config(domain2, config2)
        
        # Verify configs are separate
        assert app.get_config(domain1) == config1
        assert app.get_config(domain2) == config2
        
        # Update one domain's config
        app.update_config(domain1, {"new_key": "value"})
        
        # Verify only that domain was updated
        assert app.get_config(domain1) == {"api_key": "12345", "new_key": "value"}
        assert app.get_config(domain2) == config2