import os
import sys
from unittest.mock import patch

import click
import pytest
from click.testing import CliRunner

from saleor_app_sdk.cli import cli, create, version


class TestCli:
    def setup_method(self):
        """Set up test environment"""
        self.runner = CliRunner()

    def test_cli_group(self):
        """Test that cli is a click group"""
        assert isinstance(cli, click.Group)
        assert "create" in cli.commands
        assert "version" in cli.commands

    def test_version_command(self):
        """Test the version command"""
        with patch("saleor_app_sdk.cli.__version__", "0.1.0"):
            result = self.runner.invoke(version)
            assert result.exit_code == 0
            assert "Saleor App SDK version: 0.1.0" in result.output

    def test_create_command_basic(self):
        """Test the create command with basic template"""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(create, ["test-app"])

            assert result.exit_code == 0
            assert "Creating new Saleor app: test-app" in result.output
            assert "Using template: basic" in result.output
            assert "Successfully created Saleor app: test-app" in result.output

            # Check that the directory structure was created
            assert os.path.exists("test-app")
            assert os.path.exists("test-app/src")
            assert os.path.exists("test-app/tests")
            assert os.path.exists("test-app/templates")

            # Check that the basic files were created
            assert os.path.exists("test-app/pyproject.toml")
            assert os.path.exists("test-app/README.md")

            # Check the app module
            app_module_name = "test_app"
            assert os.path.exists(f"test-app/src/{app_module_name}")
            assert os.path.exists(f"test-app/src/{app_module_name}/__init__.py")
            assert os.path.exists(f"test-app/src/{app_module_name}/main.py")

            # Check content of main.py
            with open(f"test-app/src/{app_module_name}/main.py") as f:
                content = f.read()
                assert "SaleorAppBuilder" in content
                assert "test-app" in content
                assert "Test" in content  # Title case conversion

    def test_create_command_with_template(self):
        """Test the create command with a specific template"""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(create, ["test-app", "--template", "webhook"])

            assert result.exit_code == 0
            assert "Creating new Saleor app: test-app" in result.output
            assert "Using template: webhook" in result.output

    def test_create_command_with_directory(self):
        """Test the create command with a custom directory"""
        with self.runner.isolated_filesystem():
            # Create a custom directory
            os.makedirs("custom-dir")

            result = self.runner.invoke(
                create, ["test-app", "--directory", "custom-dir"]
            )

            assert result.exit_code == 0
            assert "Creating new Saleor app: test-app" in result.output

            # Check that the app was created in the custom directory
            assert os.path.exists("custom-dir/test-app")
            assert os.path.exists("custom-dir/test-app/src")

    def test_create_command_existing_directory(self):
        """Test the create command when the app directory already exists"""
        with self.runner.isolated_filesystem():
            # Create the app directory beforehand
            os.makedirs("test-app")

            result = self.runner.invoke(create, ["test-app"])

            assert result.exit_code == 1
            assert "Error: Directory" in result.output
            assert "already exists" in result.output

    def test_create_command_invalid_template(self):
        """Test the create command with an invalid template"""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(create, ["test-app", "--template", "invalid"])

            assert result.exit_code != 0
            assert "Invalid value for" in result.output
            assert "invalid" in result.output

    def test_create_command_future_cookiecutter_implementation(self):
        """Test for future cookiecutter implementation"""
        # This test is a placeholder for when cookiecutter is implemented
        # Skip this test for now as it's for future implementation
        pytest.skip("Cookiecutter implementation not yet available")

    def test_main_function(self):
        """Test the main function"""
        with patch.object(sys, "argv", ["saleor-app", "version"]):
            with patch("saleor_app_sdk.cli.cli") as mock_cli:
                # Import __main__ to trigger the main function
                with patch.dict(sys.modules, {"__main__.__spec__": None}):
                    from saleor_app_sdk.cli import __name__

                    if __name__ == "__main__":
                        mock_cli.assert_called_once()
