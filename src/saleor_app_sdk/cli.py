"""
Command-line interface for Saleor App SDK
"""

import sys
from pathlib import Path

import click

from saleor_app_sdk import (
    __version__,
)


@click.group()
def cli():
    """Saleor App SDK CLI tool for creating and managing Saleor apps."""


@cli.command()
@click.argument("name")
@click.option(
    "--template",
    "-t",
    default="basic",
    type=click.Choice(["basic", "webhook", "ui"]),
    help="Template type to use",
)
@click.option("--directory", "-d", default=".", help="Directory to create the app in")
def create(name, template, directory):
    """Create a new Saleor app project."""
    click.echo(f"Creating new Saleor app: {name}")
    click.echo(f"Using template: {template}")

    # TODO: Implement actual template creation with cookiecutter
    # This would use cookiecutter to create a new app from a template
    # For now, just create a basic directory structure

    app_dir = Path(directory) / name
    if app_dir.exists():
        click.echo(f"Error: Directory {app_dir} already exists", err=True)
        sys.exit(1)

    # Create basic directory structure
    app_dir.mkdir(parents=True)
    (app_dir / "src").mkdir()
    (app_dir / "tests").mkdir()
    (app_dir / "templates").mkdir()

    # Create basic files
    with open(app_dir / "pyproject.toml", "w") as f:
        f.write(f"""[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "0.1.0"
description = "A Saleor app built with saleor-app-sdk"
requires-python = ">=3.8"
dependencies = [
    "saleor-app-sdk>=0.1.0",
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
]
""")

    with open(app_dir / "README.md", "w") as f:
        f.write(f"""# {name}

A Saleor app built with saleor-app-sdk.

## Development

1. Install dependencies:
   ```
   pip install -e .
   ```

2. Run the app:
   ```
   uvicorn src.{name.replace("-", "_")}.main:app --reload
   ```
""")

    with open(app_dir / "src" / "__init__.py", "w") as f:
        f.write("")

    app_module_name = name.replace("-", "_")
    app_module_dir = app_dir / "src" / app_module_name
    app_module_dir.mkdir()

    with open(app_module_dir / "__init__.py", "w") as f:
        f.write("")

    with open(app_module_dir / "main.py", "w") as f:
        f.write(f"""from saleor_app_sdk import (
    SaleorApp, SaleorAppBuilder, SaleorPermission,
    WebhookEventType, AppConfigMixin
)

# Create your Saleor app
app = (SaleorAppBuilder("{name}", "{name.title()}")
       .version("0.1.0")
       .about("A Saleor app built with saleor-app-sdk")
       .permissions(SaleorPermission.MANAGE_ORDERS)
       .urls(
           app_url="https://example.com/app",
           config_url="https://example.com/config"
       )
       .secret_key("your-secret-key")  # Change this in production!
       .base_url("https://example.com")
       .build())

# Access the FastAPI app
fastapi_app = app.fastapi_app

@app.get("/")
async def index():
    return {{"message": "Welcome to {name}!"}}
""")

    click.echo(f"Successfully created Saleor app: {name}")
    click.echo(f"To get started, cd into {name} and check the README.md file")


@cli.command()
def version():
    """Show the Saleor App SDK version."""
    click.echo(f"Saleor App SDK version: {__version__}")


if __name__ == "__main__":
    cli()
