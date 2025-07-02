"""
Core Saleor App class
"""

import json
import logging
import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from saleor_app_sdk.graphql.client import SaleorGraphQLClient
from saleor_app_sdk.models.app_manifest import AppManifest
from saleor_app_sdk.models.installation import AppInstallation
from saleor_app_sdk.webhooks.events import WebhookEventType
from saleor_app_sdk.webhooks.handler import WebhookHandler

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
            # Get auth_token from request data
            auth_token = data["auth_token"]

            # Get domain from request data as fallback
            request_domain = data.get("domain") or os.environ.get("SALEOR_DOMAIN", "")

            # Get saleor_api_url from environment variable
            saleor_api_url = os.environ.get("SALEOR_API_URL", "")

            # Extract domain from SALEOR_API_URL if available
            domain = request_domain  # Default to request domain
            if saleor_api_url:
                try:
                    # Remove protocol (http:// or https://)
                    domain_part = saleor_api_url.split("//")[-1]
                    # Remove path and get only domain
                    extracted_domain = domain_part.split("/")[0]
                    if extracted_domain:
                        domain = extracted_domain
                except (IndexError, ValueError) as e:
                    # If extraction fails, use domain from request
                    logger.warning("Failed to extract domain from API URL: %s", e)

            # If saleor_api_url is not set, use default from domain
            if not saleor_api_url:
                saleor_api_url = f"https://{request_domain}/graphql/"

            installation = AppInstallation(
                auth_token=auth_token,
                domain=domain,
                saleor_api_url=saleor_api_url,
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
