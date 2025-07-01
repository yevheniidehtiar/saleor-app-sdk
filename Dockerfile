FROM python:3.11-slim

WORKDIR /app

# Copy requirements files and source code needed for installation
COPY pyproject.toml setup.cfg ./
COPY src ./src

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
