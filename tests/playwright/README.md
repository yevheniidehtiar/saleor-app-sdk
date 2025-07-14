# Playwright Tests for Saleor App

This directory contains Playwright tests for the Saleor App. These tests verify that the app's UI and functionality work as expected.

## Prerequisites

Before running the tests, make sure you have:

1. Installed Playwright:
   ```bash
   pip install playwright
   playwright install
   ```

2. The Saleor App running locally:
   ```bash
   uvicorn main:app --reload
   ```

## Running the Tests

To run all tests:

```bash
pytest tests/playwright
```

To run a specific test file:

```bash
pytest tests/playwright/test_config_page.py
```

## Test Files

- `test_config_page.py`: Tests the configuration page functionality
  - Verifies that the form can be filled out and submitted
  - Checks that validation works for required fields

## Adding New Tests

When adding new tests:

1. Create a new file with the naming pattern `test_*.py`
2. Import the necessary Playwright components:
   ```python
   from playwright.sync_api import Page, expect
   ```
3. Write test functions that take a `page` parameter
4. Use the `page` object to interact with the UI
5. Use `expect` to make assertions about the UI state

## Debugging Tests

To debug tests, you can use the `--headed` flag to see the browser:

```bash
pytest tests/playwright --headed
```

You can also slow down test execution with the `--slowmo` flag:

```bash
pytest tests/playwright --headed --slowmo 500
```