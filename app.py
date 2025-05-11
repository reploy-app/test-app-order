import logging
from fastapi import FastAPI, HTTPException, status
import uvicorn
from connections import check_connections
from config import PORT, LAUNCH_MODE
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     %(message)s',
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        f"Starting Order Microservice on port: {PORT} "
        f"on mode: {LAUNCH_MODE}")
    yield


# Create FastAPI app
app = FastAPI(
    title="Order Microservice",
    description="A simple microservice that connects to PostgreSQL and Redis.",
    version="0.1.0",
    lifespan=lifespan
)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint that verifies all necessary service connections.
    Returns:
        200 OK if all connections are successful
        500 Internal Server Error if any connection fails
    """
    logger.info("Health check requested")
    results, all_healthy = await check_connections()

    result = {
        "serviceName": "Order Microservice",
        "status": None,
        "launchMode": LAUNCH_MODE,
        "services": results
    }

    if all_healthy:
        result["status"] = "healthy"
        logger.info("Health check passed: All services are available")
        return {
            "detail": result
        }
    else:
        result["status"] = "unhealthy"
        logger.error(f"Health check failed: {results}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result
        )


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns basic information about the service.
    """
    return {
        "service": "Order Microservice",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health - Check the health of the service connections"
        }
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
