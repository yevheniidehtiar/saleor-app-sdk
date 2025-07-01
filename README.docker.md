# Docker Setup for Saleor App SDK

This guide explains how to run the Saleor App SDK using Docker and expose it with Ngrok to connect to an existing Saleor backend.

## Prerequisites

- Docker and Docker Compose installed on your machine
- An Ngrok account and authtoken (sign up at [ngrok.com](https://ngrok.com))
- An existing Saleor backend instance

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/saleor/saleor-app-sdk-python.git
   cd saleor-app-sdk-python
   ```

2. Create a `.env` file in the root directory by copying the example file:
   ```bash
   cp .env.example .env
   ```

3. Update the environment variables in the `.env` file:
   - `NGROK_AUTHTOKEN`: Your Ngrok authentication token
   - `NGROK_DOMAIN`: (Optional) Your custom Ngrok domain if you have one (e.g., "your-subdomain.ngrok-free.app")
   - `SECRET_KEY`: A secure secret key for your application
   - `APP_URL`: Will be automatically set to your Ngrok URL (you'll need to update this after starting the services)
   - `CONFIG_URL`: Will be automatically set to your Ngrok URL + "/config" (you'll need to update this after starting the services)
   - `BASE_URL`: Will be automatically set to your Ngrok URL (you'll need to update this after starting the services)
   - `SALEOR_API_URL`: The GraphQL API URL of your Saleor instance (e.g., "https://your-saleor-instance.saleor.cloud/graphql/")

## Running the Application

1. Start the Docker services:
   ```bash
   docker-compose up -d
   ```

2. Check the Ngrok URL:
   ```bash
   docker-compose logs ngrok
   ```
   Look for a line like: `t=... msg="started tunnel" name=... addr=app:8000 url=https://xxxx-xx-xx-xxx-xx.ngrok.io`

3. Update the environment variables in your `.env` file with the actual Ngrok URL:
   ```
   APP_URL=https://xxxx-xx-xx-xxx-xx.ngrok.io
   CONFIG_URL=https://xxxx-xx-xx-xxx-xx.ngrok.io/config
   BASE_URL=https://xxxx-xx-xx-xxx-xx.ngrok.io
   ```

4. Restart the app service to apply the changes:
   ```bash
   docker-compose restart app
   ```

## Connecting to Saleor

1. In your Saleor Dashboard, go to Apps > Install App
2. Enter your Ngrok URL (e.g., `https://xxxx-xx-xx-xxx-xx.ngrok.io`)
3. Complete the installation process

## Accessing the Application

- Main application: `https://xxxx-xx-xx-xxx-xx.ngrok.io`
- Configuration page: `https://xxxx-xx-xx-xxx-xx.ngrok.io/config`
- Ngrok inspection interface: `http://localhost:4040`

## Stopping the Application

```bash
docker-compose down
```

## Using a Custom Ngrok Domain

If you have a custom domain with Ngrok (available on paid plans):

1. Set up your custom domain in your Ngrok dashboard at [dashboard.ngrok.com](https://dashboard.ngrok.com)
2. Add the domain to your `.env` file:
   ```
   NGROK_DOMAIN=your-subdomain.ngrok-free.app
   ```
3. Update the APP_URL, CONFIG_URL, and BASE_URL to match your custom domain:
   ```
   APP_URL=https://your-subdomain.ngrok-free.app
   CONFIG_URL=https://your-subdomain.ngrok-free.app/config
   BASE_URL=https://your-subdomain.ngrok-free.app
   ```
4. Start or restart the services:
   ```bash
   docker-compose up -d
   ```

## Troubleshooting

- If you're having issues with the Ngrok connection, make sure your authtoken is correct and that you've updated the environment variables with the correct Ngrok URL.
- If using a custom domain, ensure it's properly set up in your Ngrok dashboard and that your account plan supports custom domains.
- Check the logs for any errors:
  ```bash
  docker-compose logs app
  docker-compose logs ngrok
  ```
