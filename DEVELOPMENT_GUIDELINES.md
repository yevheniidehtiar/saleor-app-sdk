# Development Guidelines for Saleor App SDK Python

This document outlines the development guidelines and best practices for contributing to the Saleor App SDK for Python project. These guidelines ensure code consistency, maintainability, and quality across the entire codebase.

## Table of Contents

1. [Code Style and Standards](#code-style-and-standards)
2. [Architecture Patterns](#architecture-patterns)
3. [Testing Guidelines](#testing-guidelines)
4. [Documentation Standards](#documentation-standards)
5. [Git Workflow](#git-workflow)
6. [Performance Considerations](#performance-considerations)
7. [Security Best Practices](#security-best-practices)
8. [Error Handling](#error-handling)
9. [Logging Guidelines](#logging-guidelines)
10. [Dependency Management](#dependency-management)

## Code Style and Standards

### Python Version Support
- **Minimum Python Version**: 3.11+
- **Target Python Versions**: 3.11, 3.12, 3.13
- Always use modern Python features when appropriate

### Code Formatting and Linting
- **Formatter**: Use `ruff` for code formatting
- **Linter**: Use `ruff` for linting
- **Type Checker**: Use `mypy` for static type checking
- **Pre-commit Hooks**: Always use pre-commit hooks to ensure code quality

### Type Hints
- **Required**: All public functions, methods, and class attributes must have type hints
- **Union Types**: Use `|` syntax for union types (e.g., `str | None` instead of `Optional[str]`)
- **Generic Types**: Use proper generic type hints for collections and custom classes

```python
# Good
def get_installation(self, domain: str) -> AppInstallation | None:
    return self.installations.get(domain)

# Bad
def get_installation(self, domain):
    return self.installations.get(domain)
```

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

### Dependency Injection
- Use dependency injection for testability
- Avoid hard-coded dependencies
- Use FastAPI's dependency injection system when appropriate

### Separation of Concerns
- **Core Logic**: Keep business logic separate from FastAPI routes
- **Models**: Use Pydantic models for data validation and serialization
- **Services**: Create service classes for complex operations
- **Handlers**: Use dedicated handler classes for webhooks and events

### Error Handling Strategy
- Use custom exception classes for domain-specific errors
- Implement proper error propagation
- Provide meaningful error messages to developers

## Testing Guidelines

### Test Structure
- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Use Playwright for UI testing
- **Test Coverage**: Maintain minimum 80% test coverage

### Test Organization
```
tests/
├── unit/
│   ├── app/
│   ├── graphql/
│   ├── models/
│   └── webhooks/
└── playwright/
    └── ui_tests/
```

### Testing Best Practices
- Use `pytest` as the testing framework
- Use `pytest-asyncio` for async test support
- Mock external dependencies (HTTP calls, database operations)
- Use fixtures for common test data
- Write descriptive test names that explain the scenario

```python
# Good test name
def test_webhook_handler_processes_order_created_event_successfully():
    pass

# Bad test name
def test_webhook():
    pass
```

### Playwright Testing
- Test critical user flows
- Use page object pattern for complex UI interactions
- Run tests in multiple browsers when necessary
- Include visual regression testing for UI components

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

### API Documentation
- Use FastAPI's automatic OpenAPI documentation
- Add detailed descriptions to route handlers
- Include request/response examples

## Git Workflow

### Branch Naming
- **Feature branches**: `feature/description-of-feature`
- **Bug fixes**: `fix/description-of-fix`
- **Documentation**: `docs/description-of-changes`
- **Refactoring**: `refactor/description-of-refactor`

### Commit Messages
- Use conventional commit format
- Include scope when relevant
- Write clear, descriptive commit messages

```
feat(webhooks): add support for product variant events
fix(graphql): handle connection timeout errors
docs(readme): update installation instructions
```

### Pull Request Guidelines
- Create focused PRs that address single concerns
- Include comprehensive PR descriptions
- Add tests for new functionality
- Update documentation when necessary
- Ensure all CI checks pass

## Performance Considerations

### Async/Await Usage
- Use async/await for I/O operations
- Avoid blocking operations in async contexts
- Use proper connection pooling for HTTP clients

### Memory Management
- Avoid memory leaks in long-running applications
- Use generators for large data processing
- Implement proper cleanup in context managers

### Caching Strategy
- Cache expensive operations when appropriate
- Use TTL-based caching for external API calls
- Implement cache invalidation strategies

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

## Error Handling

### Exception Hierarchy
```python
class SaleorAppError(Exception):
    """Base exception for Saleor App SDK"""
    pass

class WebhookError(SaleorAppError):
    """Webhook processing errors"""
    pass

class GraphQLError(SaleorAppError):
    """GraphQL client errors"""
    pass
```

### Error Response Format
- Use consistent error response format
- Include error codes for programmatic handling
- Provide helpful error messages for developers

## Logging Guidelines

### Logging Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General operational information
- **WARNING**: Potentially harmful situations
- **ERROR**: Error events that might still allow the application to continue
- **CRITICAL**: Serious error events that might cause the application to abort

### Logging Best Practices
- Use structured logging when possible
- Include relevant context in log messages
- Avoid logging sensitive information
- Use appropriate log levels

```python
import logging

logger = logging.getLogger(__name__)

# Good logging
logger.info("Processing webhook for domain: %s", domain)
logger.error("Failed to process webhook: %s", str(error), exc_info=True)

# Bad logging
logger.info(f"Processing webhook for {domain}")
logger.error("Error occurred")
```

## Dependency Management

### Dependency Categories
- **Core Dependencies**: Essential for basic functionality
- **Optional Dependencies**: Feature-specific dependencies
- **Development Dependencies**: Testing, linting, documentation tools

### Version Pinning
- Pin major versions for stability
- Allow minor version updates for bug fixes
- Regularly update dependencies for security patches

### Dependency Review
- Review new dependencies for security and maintenance status
- Prefer well-maintained packages with active communities
- Consider the impact on bundle size and performance

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

### Documentation
- Explain the purpose and use case of each example
- Provide step-by-step setup instructions
- Include troubleshooting sections
- Document any external dependencies or services required

---

## Contributing

When contributing to this project:

1. Read and follow these guidelines
2. Set up pre-commit hooks: `pre-commit install`
3. Run tests before submitting: `pytest`
4. Check code quality: `ruff check` and `mypy`
5. Update documentation when necessary
6. Write meaningful commit messages
7. Create focused pull requests

For questions about these guidelines or suggestions for improvements, please open an issue or start a discussion in the repository.