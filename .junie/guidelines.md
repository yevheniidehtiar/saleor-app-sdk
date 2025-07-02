# Junie Guidelines for Saleor App SDK Python

This document provides guidelines for Junie when working with the Saleor App SDK for Python project. These guidelines ensure code consistency, maintainability, and quality across the entire codebase.

## Project Structure

The project follows a standard Python package structure:

```
src/saleor_app_sdk/          # Main SDK package
├── app/                     # Core app functionality
├── graphql/                 # GraphQL client and queries
├── models/                  # Pydantic models
└── webhooks/                # Webhook handling

scaffold/                    # Saleor-app template (Copier + Jinja) 

tests/                       # Test suite
├── unit/                    # Unit tests
└── playwright/              # End-to-end tests
```

## Testing Requirements

**Junie MUST run tests to verify correctness of proposed solutions.**

### Running Tests
- Use `pytest` to run unit tests: `pytest tests/unit/`
- Maintain minimum 80% test coverage
- Run specific test modules when making targeted changes
- For UI changes, consider running Playwright tests: `pytest tests/playwright/`

### Test Organization
- Unit tests mirror the source code structure
- Each module should have corresponding tests
- Use descriptive test names that explain the scenario
- Mock external dependencies (HTTP calls, database operations)

## Code Style and Standards

### Python Version Support
- **Minimum Python Version**: 3.11+
- **Target Python Versions**: 3.11, 3.12, 3.13

### Code Quality Tools
- **Formatter**: Use `ruff` for code formatting
- **Linter**: Use `ruff` for linting  
- **Type Checker**: Use `mypy` for static type checking
- Run quality checks: `ruff check` and `mypy`

### Type Hints
- **Required**: All public functions, methods, and class attributes must have type hints
- **Union Types**: Use `|` syntax for union types (e.g., `str | None` instead of `Optional[str]`)
- **Generic Types**: Use proper generic type hints for collections and custom classes

### Naming Conventions
- **Classes**: PascalCase (e.g., `SaleorApp`, `WebhookHandler`)
- **Functions/Methods**: snake_case (e.g., `get_installation`, `process_webhook`)
- **Variables**: snake_case (e.g., `auth_token`, `saleor_api_url`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`, `MAX_RETRIES`)
- **Private Methods**: Prefix with single underscore (e.g., `_setup_core_routes`)

### Docstrings
- Use Google-style docstrings for all public classes and methods
- Include type information in docstrings when it adds clarity
- Provide examples for complex functions

```python
def get_graphql_client(self, domain: str) -> SaleorGraphQLClient | None:
    """Get GraphQL client for specific installation.

    Args:
        domain: The domain of the Saleor installation

    Returns:
        SaleorGraphQLClient instance if installation exists, None otherwise

    Example:
        >>> app = SaleorApp(manifest, secret_key)
        >>> client = app.get_graphql_client("example.saleor.cloud")
    """
```

## Architecture Patterns

### Builder Pattern
- Use the Builder pattern for complex object construction (e.g., `SaleorAppBuilder`)
- Provide fluent interfaces for better developer experience
- Validate configuration at build time

### Separation of Concerns
- **Core Logic**: Keep business logic separate from FastAPI routes
- **Models**: Use Pydantic models for data validation and serialization
- **Services**: Create service classes for complex operations
- **Handlers**: Use dedicated handler classes for webhooks and events

### Error Handling Strategy
- Use custom exception classes for domain-specific errors
- Implement proper error propagation
- Provide meaningful error messages to developers

## Security Best Practices

### Authentication and Authorization
- Validate webhook signatures
- Use secure token storage
- Implement proper CORS policies
- Validate all input data

### Environment Variables
- Use environment variables for sensitive configuration
- Provide secure defaults
- Document all required environment variables

### Data Handling
- Sanitize user inputs
- Use parameterized queries for database operations
- Implement proper data validation

## Performance Considerations

### Async/Await Usage
- Use async/await for I/O operations
- Avoid blocking operations in async contexts
- Use proper connection pooling for HTTP clients

### Memory Management
- Avoid memory leaks in long-running applications
- Use generators for large data processing
- Implement proper cleanup in context managers

## Documentation Standards

### Code Documentation
- Document all public APIs
- Include usage examples in docstrings
- Explain complex algorithms and business logic
- Keep documentation up-to-date with code changes

### README Files
- Each app example should have its own README
- Include setup instructions, usage examples, and configuration details
- Provide troubleshooting sections for common issues

## Build Requirements

**Junie should NOT build the project before submitting results** unless specifically requested. The project uses:
- `uv` for dependency management
- Standard Python packaging with `pyproject.toml`
- FastAPI for web applications

## App Examples Guidelines

### Structure
- Each app example should be self-contained
- Include comprehensive README with setup instructions
- Provide example configuration files
- Include sample data when appropriate

### Code Quality
- Follow the same coding standards as the main SDK
- Include proper error handling
- Add logging for debugging purposes
- Write tests for critical functionality

## Quality Checklist

Before submitting changes, ensure:

1. ✅ All tests pass: `pytest`
2. ✅ Code quality checks pass: `ruff check` and `mypy`
3. ✅ Type hints are present for all public APIs
4. ✅ Docstrings are added for new public methods/classes
5. ✅ Tests are added for new functionality
6. ✅ Documentation is updated when necessary
7. ✅ Security best practices are followed
8. ✅ Performance considerations are addressed
