import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from saleor_app_sdk.models.installation import AppInstallation


class TestAppInstallation:
    def test_init_minimal(self, auth_token, domain, saleor_api_url):
        """Test initialization with minimal required fields"""
        installation = AppInstallation(
            auth_token=auth_token,
            domain=domain,
            saleor_api_url=saleor_api_url,
        )

        assert installation.auth_token == auth_token
        assert installation.domain == domain
        assert installation.saleor_api_url == saleor_api_url
        assert isinstance(installation.installed_at, datetime)

    def test_init_with_installed_at(self, auth_token, domain, saleor_api_url):
        """Test initialization with custom installed_at"""
        installed_at = datetime(2023, 1, 1, 12, 0, 0)

        installation = AppInstallation(
            auth_token=auth_token,
            domain=domain,
            saleor_api_url=saleor_api_url,
            installed_at=installed_at,
        )

        assert installation.installed_at == installed_at

    def test_construct_saleor_api_url_from_domain(self, auth_token, domain):
        """Test constructing saleor_api_url from domain"""
        # Construct saleor_api_url from domain
        constructed_api_url = f"https://{domain}/graphql/"

        installation = AppInstallation(
            auth_token=auth_token,
            domain=domain,
            saleor_api_url=constructed_api_url,
        )

        assert installation.auth_token == auth_token
        assert installation.domain == domain
        assert installation.saleor_api_url == constructed_api_url

    def test_validation_auth_token_required(self, domain, saleor_api_url):
        """Test validation error when auth_token is missing"""
        with pytest.raises(ValidationError):
            AppInstallation(
                domain=domain,
                saleor_api_url=saleor_api_url,
            )

    def test_validation_domain_required(self, auth_token, saleor_api_url):
        """Test validation error when domain is missing"""
        with pytest.raises(ValidationError):
            AppInstallation(
                auth_token=auth_token,
                saleor_api_url=saleor_api_url,
            )

    def test_validation_saleor_api_url_required(self, auth_token, domain):
        """Test validation error when saleor_api_url is missing"""
        with pytest.raises(ValidationError):
            AppInstallation(
                auth_token=auth_token,
                domain=domain,
                saleor_api_url=None,
            )

    def test_model_config_extra_forbid(self, auth_token, domain, saleor_api_url):
        """Test that extra fields are forbidden"""
        with pytest.raises(ValidationError):
            AppInstallation(
                auth_token=auth_token,
                domain=domain,
                saleor_api_url=saleor_api_url,
                extra_field="value",  # This should cause a validation error
            )

    def test_dict_conversion(self, auth_token, domain, saleor_api_url):
        """Test conversion to dict"""
        installed_at = datetime(2023, 1, 1, 12, 0, 0)

        installation = AppInstallation(
            auth_token=auth_token,
            domain=domain,
            saleor_api_url=saleor_api_url,
            installed_at=installed_at,
        )

        installation_dict = installation.model_dump()

        assert installation_dict["auth_token"] == auth_token
        assert installation_dict["domain"] == domain
        assert installation_dict["saleor_api_url"] == saleor_api_url
        assert installation_dict["installed_at"] == installed_at

    def test_json_serialization(self, auth_token, domain, saleor_api_url):
        """Test JSON serialization"""
        installed_at = datetime(2023, 1, 1, 12, 0, 0)

        installation = AppInstallation(
            auth_token=auth_token,
            domain=domain,
            saleor_api_url=saleor_api_url,
            installed_at=installed_at,
        )

        json_str = installation.model_dump_json()

        assert auth_token in json_str
        assert domain in json_str
        assert saleor_api_url in json_str
        assert "2023-01-01T12:00:00" in json_str

    def test_equality(self, auth_token, domain, saleor_api_url):
        """Test equality comparison"""
        installed_at = datetime(2023, 1, 1, 12, 0, 0)

        installation1 = AppInstallation(
            auth_token=auth_token,
            domain=domain,
            saleor_api_url=saleor_api_url,
            installed_at=installed_at,
        )

        installation2 = AppInstallation(
            auth_token=auth_token,
            domain=domain,
            saleor_api_url=saleor_api_url,
            installed_at=installed_at,
        )

        assert installation1 == installation2

        # Test inequality
        installation3 = AppInstallation(
            auth_token="different-token",
            domain=domain,
            saleor_api_url=saleor_api_url,
            installed_at=installed_at,
        )

        assert installation1 != installation3
