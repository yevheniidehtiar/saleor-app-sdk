"""
Core Saleor App class
"""

import json
import logging

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from ..graphql.client import SaleorGraphQLClient
from ..models.app_manifest import AppManifest
from ..models.installation import AppInstallation
from ..webhooks.events import WebhookEventType
from ..webhooks.handler import WebhookHandler

logger = logging.getLogger(__name__)


class SaleorApp:
    """Main Saleor App class - the core of the SDK"""

    def __init__(
        self,
        manifest: AppManifest,
        secret_key: str,
        base_url: str | None = None,
        templates_dir: str = "templates",
    ):
        self.manifest = manifest
        self.secret_key = secret_key
        self.base_url = base_url
        self.fastapi_app = FastAPI(title=manifest.name)
        self.templates = Jinja2Templates(directory=templates_dir)
        self.webhook_handler = WebhookHandler(secret_key)
        self.installations: dict[str, AppInstallation] = {}

        # Setup core routes
        self._setup_core_routes()

    def _setup_core_routes(self):
        """Setup core SDK routes"""

        @self.fastapi_app.get("/api/manifest")
        async def get_manifest():
            return self._serialize_manifest()

        @self.fastapi_app.post("/api/register")
        async def register_installation(request: Request):
            body = await request.body()
            data = json.loads(body)

            installation = AppInstallation(
                auth_token=data["auth_token"],
                domain=data["domain"],
                saleor_api_url=data.get(
                    "saleor_api_url", f"https://{data['domain']}/graphql/"
                ),
            )

            self.installations[installation.domain] = installation

            # Call custom installation handler if defined
            if hasattr(self, "on_install"):
                await self.on_install(installation)

            return {"success": True}

        @self.fastapi_app.post("/api/webhooks/{event_type}")
        async def handle_webhook(_event_type: str, request: Request):
            return await self.webhook_handler.process_webhook(request)

    def _serialize_manifest(self) -> dict:
        """Serialize app manifest to dict"""
        manifest_dict = {
            "id": self.manifest.id,
            "name": self.manifest.name,
            "version": self.manifest.version,
            "about": self.manifest.about,
            "permissions": [p.value for p in self.manifest.permissions],
            "appUrl": self.manifest.app_url,
            "tokenTargetUrl": f"{self.base_url}/api/register",
            "webhooks": [],
        }

        if self.manifest.configuration_url:
            manifest_dict["configurationUrl"] = self.manifest.configuration_url
        if self.manifest.data_privacy_url:
            manifest_dict["dataPrivacyUrl"] = self.manifest.data_privacy_url
        if self.manifest.homepage_url:
            manifest_dict["homepageUrl"] = self.manifest.homepage_url
        if self.manifest.support_url:
            manifest_dict["supportUrl"] = self.manifest.support_url

        # Add webhooks
        if self.manifest.webhooks:
            for webhook in self.manifest.webhooks:
                manifest_dict["webhooks"].append(
                    {
                        "name": webhook.name,
                        "asyncEvents": [e.value for e in webhook.events],
                        "query": webhook.query,
                        "targetUrl": webhook.target_url,
                        "isActive": webhook.is_active,
                    }
                )

        return manifest_dict

    def get_installation(self, domain: str) -> AppInstallation | None:
        """Get app installation by domain"""
        return self.installations.get(domain)

    def get_graphql_client(self, domain: str) -> SaleorGraphQLClient | None:
        """Get GraphQL client for specific installation"""
        installation = self.get_installation(domain)
        if installation:
            return SaleorGraphQLClient(
                installation.saleor_api_url, installation.auth_token
            )
        return None

    # Decorators for common patterns
    def route(self, path: str, **kwargs):
        """Add custom route to the app"""
        return self.fastapi_app.route(path, **kwargs)

    def get(self, path: str, **kwargs):
        return self.fastapi_app.get(path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.fastapi_app.post(path, **kwargs)

    def webhook(self, event_type: WebhookEventType):
        """Decorator for webhook handlers"""
        return self.webhook_handler.on(event_type)

    async def on_install(self, installation: AppInstallation):
        """Override this method to handle app installation"""

    async def on_uninstall(self, installation: AppInstallation):
        """Override this method to handle app uninstall"""
