"""
Configuration mixin for Saleor apps
"""


class AppConfigMixin:
    """Mixin for apps that need configuration storage"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_storage: dict[str, dict] = {}

    def get_config(self, domain: str, default: dict | None = None) -> dict:
        return self.config_storage.get(domain, default or {})

    def set_config(self, domain: str, config: dict):
        self.config_storage[domain] = config

    def update_config(self, domain: str, updates: dict):
        current = self.get_config(domain, {})
        current.update(updates)
        self.set_config(domain, current)
