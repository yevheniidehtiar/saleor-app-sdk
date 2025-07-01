"""
App installation model for Saleor App SDK
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppInstallation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    auth_token: str
    domain: str
    saleor_api_url: str
    installed_at: datetime = datetime.utcnow()
