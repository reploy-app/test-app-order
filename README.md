# OrderService Microservice

A simple Python microservice to test multi repo projects and dynamically created .env files. 

This service connects to private PostgreSQL and shared to test dynamically created .env and run configurations.

A run configuration is esentially a way to launch a service. This might include different cases such as passing different arguments to a command or running an entirely different command for different purposes. 

For example, one might want to launch a django app but before that they might want to run migrations. These two operations are executed in the same repository but with different commands. Each of the commands maps to their own run configuration, so you have two distinct ways to use a repository. 

To test the connectivity, simply connect to healthcheck endpoint to see if all dependenices are reachable.

The same endpoint returns the value of --launch-mode argument so that testing code can tell if run configuration is taking effect. 


## Features

- PostgreSQL database connection
- Redis connection
- Health check endpoint that verifies all connections
- Environment variable configuration

## Requirements

- Python 3.13
- PostgreSQL database
- Redis server

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd order-service
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the environment variables:

Copy the example environment file and modify it according to your setup:

```bash
cp .env.example .env
```

Edit the `.env` file to add the appropriate connection details for your services.


## Running the Service

Start the service with:

```bash
python app.py
```

You can specify the launch mode with the `--launch-mode` parameter:

```bash
python app.py --launch-mode worker
```

Available launch modes:
- `api` (default): Run as an API service
- `worker`: Run as a background worker

Or using uvicorn directly:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

To pass the launch mode when using uvicorn, you need to modify your configuration to read environment variables:

```bash
LAUNCH_MODE=worker uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check

`GET /health`

Returns a status of all service connections:
- 200 OK if all connections are good
- 500 Internal Server Error if any connection fails

Example response (all healthy):

```json
{
  "detail": {
    "serviceName": "Order Microservice",
    "status": "healthy",
    "launchMode": "worker",
    "services": {
      "postgres": false,
      "redis": false
    }
  }
}
```

### Root

`GET /`

Returns basic information about the service.

Example response:

```json
{
  "service": "OrderService Microservice",
  "version": "0.1.0",
  "endpoints": {
    "health": "/health - Check the health of the service connections"
  }
}
```

## Docker Deployment (Optional)

A Dockerfile is provided for containerized deployment.

Build the Docker image:

```bash
docker build -t order-service .
```

Run the container:

```bash
docker run -p 8000:8000 --env-file .env order-service
```

To specify the launch mode when running Docker:

```bash
docker run -p 8000:8000 --env-file .env order-service --launch-mode worker
```
