import pytest
from enum import Enum

from saleor_app_sdk.permissions import SaleorPermission


class TestSaleorPermission:
    def test_is_enum(self):
        """Test that SaleorPermission is an Enum"""
        assert issubclass(SaleorPermission, Enum)
        assert issubclass(SaleorPermission, str)

    def test_order_permissions(self):
        """Test order-related permissions"""
        assert SaleorPermission.MANAGE_ORDERS == "MANAGE_ORDERS"
        assert SaleorPermission.MANAGE_CHECKOUTS == "MANAGE_CHECKOUTS"
        assert SaleorPermission.HANDLE_PAYMENTS == "HANDLE_PAYMENTS"

    def test_product_permissions(self):
        """Test product-related permissions"""
        assert SaleorPermission.MANAGE_PRODUCTS == "MANAGE_PRODUCTS"
        assert SaleorPermission.MANAGE_GIFT_CARD == "MANAGE_GIFT_CARD"

    def test_user_permissions(self):
        """Test user-related permissions"""
        assert SaleorPermission.MANAGE_USERS == "MANAGE_USERS"
        assert SaleorPermission.MANAGE_STAFF == "MANAGE_STAFF"

    def test_content_permissions(self):
        """Test content-related permissions"""
        assert SaleorPermission.MANAGE_PAGES == "MANAGE_PAGES"
        assert SaleorPermission.MANAGE_MENUS == "MANAGE_MENUS"
        assert SaleorPermission.MANAGE_TRANSLATIONS == "MANAGE_TRANSLATIONS"

    def test_settings_permissions(self):
        """Test settings-related permissions"""
        assert SaleorPermission.MANAGE_SETTINGS == "MANAGE_SETTINGS"
        assert SaleorPermission.MANAGE_CHANNELS == "MANAGE_CHANNELS"
        assert SaleorPermission.MANAGE_DISCOUNTS == "MANAGE_DISCOUNTS"
        assert SaleorPermission.MANAGE_PLUGINS == "MANAGE_PLUGINS"

    def test_all_permissions_are_strings(self):
        """Test that all permission values are strings"""
        for permission in SaleorPermission:
            assert isinstance(permission.value, str)
            assert permission.value == permission.name

    def test_enum_comparison(self):
        """Test comparing enum values"""
        assert SaleorPermission.MANAGE_ORDERS == SaleorPermission.MANAGE_ORDERS
        assert SaleorPermission.MANAGE_ORDERS != SaleorPermission.MANAGE_PRODUCTS
        assert SaleorPermission.MANAGE_ORDERS == "MANAGE_ORDERS"
        assert SaleorPermission.MANAGE_ORDERS != "MANAGE_PRODUCTS"

    def test_enum_in_list(self):
        """Test using enum values in lists"""
        permissions = [SaleorPermission.MANAGE_ORDERS, SaleorPermission.MANAGE_PRODUCTS]
        assert SaleorPermission.MANAGE_ORDERS in permissions
        assert SaleorPermission.MANAGE_USERS not in permissions
        assert "MANAGE_ORDERS" in [p.value for p in permissions]

    def test_enum_as_dict_key(self):
        """Test using enum values as dictionary keys"""
        permissions_dict = {
            SaleorPermission.MANAGE_ORDERS: "Can manage orders",
            SaleorPermission.MANAGE_PRODUCTS: "Can manage products",
        }
        assert permissions_dict[SaleorPermission.MANAGE_ORDERS] == "Can manage orders"
        assert SaleorPermission.MANAGE_ORDERS in permissions_dict
        assert SaleorPermission.MANAGE_USERS not in permissions_dict

    def test_enum_iteration(self):
        """Test iterating over enum values"""
        permissions = list(SaleorPermission)
        assert len(permissions) == 14  # Update this if more permissions are added
        assert SaleorPermission.MANAGE_ORDERS in permissions
        assert SaleorPermission.MANAGE_PRODUCTS in permissions
        assert SaleorPermission.MANAGE_USERS in permissions

    def test_from_string(self):
        """Test creating enum values from strings"""
        assert SaleorPermission("MANAGE_ORDERS") == SaleorPermission.MANAGE_ORDERS
        assert SaleorPermission("MANAGE_PRODUCTS") == SaleorPermission.MANAGE_PRODUCTS

        with pytest.raises(ValueError):
            SaleorPermission("INVALID_PERMISSION")
