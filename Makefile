.PHONY: help install install-dev test lint format type-check clean build docs

help:  ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install package for production
	uv pip install -e .

install-dev:  ## Install package with development dependencies
	uv pip install -e .[dev]

test:  ## Run tests
	pytest -vv

test-coverage:  ## Run tests with coverage
	pytest --cov=saleor_app_sdk --cov-report=html --cov-report=term

lint:  ## Run linting
	@ruff check src tests

format:  ## Format code
	@ruff format src tests
	@ruff check --fix --unsafe-fixes src tests

type-check:  ## Run type checking
	mypy src

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python -m build

docs:  ## Build documentation
	mkdocs build

docs-serve:  ## Serve documentation locally
	mkdocs serve
