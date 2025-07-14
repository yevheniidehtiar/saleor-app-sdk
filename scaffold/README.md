# Saleor App Scaffold

This is a [Copier](https://copier.readthedocs.io/) template for creating Saleor apps using the [Saleor App SDK for Python](https://github.com/saleor/saleor-app-sdk-python).

## Features

- 🚀 **FastAPI-based**: Built on top of FastAPI for high performance
- 🔧 **Saleor SDK Integration**: Pre-configured with saleor-app-sdk
- 🐳 **Docker Support**: Optional Docker and docker-compose configuration
- 🧪 **Testing Setup**: Optional pytest configuration with coverage
- 📝 **Code Quality**: Pre-configured with ruff, mypy, and other tools
- 📦 **Modern Python**: Supports Python 3.11, 3.12, and 3.13
- 🔒 **Security**: Built-in security best practices
- 📚 **Documentation**: Comprehensive README and inline documentation

## Requirements

- Python 3.11+
- [Copier](https://copier.readthedocs.io/) (`pip install copier`)

## Usage

### Generate a new Saleor app

```bash
copier copy https://github.com/yevheniidehtiar/saleor-app-sdk-py/saleor-app-scaffold my-new-saleor-app
```

### Update an existing app

```bash
cd my-existing-saleor-app
copier update
```

## Template Variables

The template will prompt you for the following information:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `app_name` | App name (kebab-case) | `my-saleor-app` | `inventory-manager` |
| `app_display_name` | Display name | Auto-generated | `Inventory Manager` |
| `app_description` | Brief description | `A Saleor app built with saleor-app-sdk` | `Manages inventory across multiple warehouses` |
| `app_version` | Initial version | `0.1.0` | `1.0.0` |
| `author_name` | Your name | - | `John Doe` |
| `author_email` | Your email | - | `john@example.com` |
| `python_version` | Python version | `3.11` | `3.12` |
| `include_docker` | Include Docker config | `true` | `false` |
| `include_tests` | Include test setup | `true` | `false` |
| `saleor_permissions` | Required permissions | `MANAGE_ORDERS` | `MANAGE_ORDERS, MANAGE_PRODUCTS` |
| `app_url` | App URL | `https://example.com` | `https://myapp.herokuapp.com` |

## Generated Project Structure

```
my-saleor-app/
├── src/
│   └── my_saleor_app/
│       ├── __init__.py
│       └── main.py
├── tests/                  # If include_tests=true
│   ├── __init__.py
│   └── test_main.py
├── docker-compose.yml      # If include_docker=true
├── Dockerfile              # If include_docker=true
├── pyproject.toml
├── README.md
├── LICENSE
├── Makefile
├── .env.example
└── .gitignore
```

## Development Workflow

After generating your app:

1. **Navigate to your app directory**:
   ```bash
   cd my-new-saleor-app
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Install dependencies**:
   ```bash
   make install
   # Or with dev dependencies: make dev-install
   ```

4. **Run the app**:
   ```bash
   make run
   # Or with Docker: make docker-run
   ```

5. **Run tests** (if included):
   ```bash
   make test
   ```

## Customization

### Adding New Features

The generated app provides a solid foundation. You can extend it by:

- Adding new endpoints in `src/your_app/main.py`
- Implementing webhook handlers
- Adding database models and migrations
- Integrating with external services

### Configuration

The app uses environment variables for configuration. See `.env.example` for available options.

### Docker Development

If you included Docker support, you can use:

```bash
make docker-build  # Build the image
make docker-run    # Run with docker-compose
make docker-stop   # Stop containers
make docker-logs   # View logs
```

## Best Practices

1. **Security**: Always change the default secret key in production
2. **Environment Variables**: Use `.env` files for configuration
3. **Testing**: Write tests for your endpoints and business logic
4. **Code Quality**: Use the provided linting and formatting tools
5. **Documentation**: Keep your README updated as you add features

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've installed the package with `pip install -e .`
2. **Permission Errors**: Ensure your Saleor permissions match your app's needs
3. **Docker Issues**: Check that Docker is running and ports aren't conflicting

### Getting Help

- Check the [Saleor App SDK documentation](https://github.com/saleor/saleor-app-sdk-python)
- Review the generated README.md in your app
- Open an issue in the scaffold repository

## Contributing

To contribute to this scaffold:

1. Fork the repository
2. Make your changes
3. Test with different template configurations
4. Submit a pull request

## License

This scaffold is licensed under the MIT License. Generated apps will also use the MIT License by default.