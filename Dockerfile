# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app


# Install system dependencies for unixODBC and ODBC drivers
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    libodbc1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file (assuming you have one)
COPY requirements.txt ./

# Install Python dependencies, including pyodbc
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--ssl-keyfile=config/key.pem", "--ssl-certfile=config/cert.pem", "--reload"]